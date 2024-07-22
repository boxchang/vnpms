import json
from datetime import datetime, timedelta
import xlwt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from inventory.models import ItemCategory, ItemType, Item, Series
from stock.forms import StorageEditForm, LocationEditForm, BinEditForm, ItemSearchForm, BinSearchForm, \
    StockInPForm, StockOutPForm, StockHistoryForm, RecentHistoryForm, StockSearchForm
from stock.models import Storage, Location, Bin, StockHistory, StockInForm, StockOutForm, Stock

# 滾序號
from stock.utils import Do_Transaction


def get_series_number(_key, _key_name):
    obj = Series.objects.filter(key=_key)
    if obj:
        _series = obj[0].series + 1
        obj.update(series=_series, desc=_key_name)
    else:
        _series = 1
        Series.objects.create(key=_key, series=1, desc=_key_name)
    return _series


# Storage 編輯
@login_required
def storage_edit(request):
    form = StorageEditForm()
    if request.method == 'POST':
        pk = request.POST.get('pk')
        action = request.POST.get('action')
        storage = Storage.objects.get(pk=pk)
        if action == "edit":
            form = StorageEditForm(request.POST, instance=storage)
            if form.is_valid():
                tmp_form = form.save(commit=False)
                tmp_form.update_by = request.user
                tmp_form.save()
                return redirect(reverse('location_setting'))

        else:
            form = StorageEditForm(instance=storage)

    return render(request, 'stock/storage_edit.html', locals())


def search(request):
    return render(request, 'stock/search.html', locals())

# Storage 編輯
@login_required
def location_setting(request):
    storages = Storage.objects.all()
    return render(request, 'stock/storage.html', locals())


# Location 編輯
@login_required
def location_list(request):
    if request.method == 'POST':
        storage_code = request.POST.get('pk')
        storage = Storage.objects.get(storage_code=storage_code)
        locations = Location.objects.filter(storage=storage).all()
    return render(request, 'stock/location.html', locals())


# Location 編輯
@login_required
def location_add(request):
    if request.method == 'POST':
        storage_code = request.POST.get('storage_code')
        storage = Storage.objects.get(storage_code=storage_code)
        form = LocationEditForm(initial={'storage': storage})
        form.fields['storage'].widget.attrs['disabled'] = True
        action = "add"
        return render(request, 'stock/location_edit.html', locals())


# Location 編輯
@login_required
def location_edit(request):
    if request.method == 'POST':
        storage_code = request.POST.get('storage_code')
        location_code = request.POST.get('location_code')
        if location_code:
            location = Location.objects.get(location_code=location_code)
        form = LocationEditForm(instance=location)
        form.fields['plant'].widget.attrs['disabled'] = True
        form.fields['storage'].widget.attrs['disabled'] = True
        form.fields['location_code'].widget.attrs['readonly'] = True
        action = "edit"
        return render(request, 'stock/location_edit.html', locals())


# Location 編輯
@login_required
def location_save(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == "edit":
            location_code = request.POST.get('location_code')
            if location_code:
                location = Location.objects.get(location_code=location_code)

            form = LocationEditForm(request.POST, instance=location)
            if form.is_valid():
                tmp_form = form.save(commit=False)
                tmp_form.update_by = request.user
                tmp_form.save()
        elif action == "add":
            form = LocationEditForm(request.POST)
            if form.is_valid():
                tmp_form = form.save(commit=False)
                tmp_form.update_by = request.user
                tmp_form.save()

        storage_code = request.POST.get('storage_code')
        storage = Storage.objects.get(storage_code=storage_code)
        locations = Location.objects.filter(storage=storage).all()
        return render(request, 'stock/location.html', locals())
    return render(request, 'stock/location_edit.html', locals())

# 儲格編輯
@login_required
def bin_list(request, storage_code, location_code):
    bins = Bin.objects.filter(location=location_code).all()
    return render(request, 'stock/bin.html', locals())


# 儲格編輯
@login_required
def bin_add(request):
    if request.method == 'POST':
        storage_code = request.POST.get('storage_code')
        location_code = request.POST.get('location_code')
        location = Location.objects.get(location_code=location_code)
        form = BinEditForm(initial={'location': location})
        form.fields['location'].widget.attrs['disabled'] = True
        action = "add"
        return render(request, 'stock/bin_edit.html', locals())


# 儲格編輯
@login_required
def bin_edit(request):
    if request.method == 'POST':
        storage_code = request.POST.get('storage_code')
        location_code = request.POST.get('location_code')
        bin_code = request.POST.get('bin_code')
        if bin_code:
            bin = Bin.objects.get(bin_code=bin_code)
        form = BinEditForm(instance=bin)
        form.fields['location'].widget.attrs['disabled'] = True
        form.fields['bin_code'].widget.attrs['readonly'] = True
        action = "edit"
        return render(request, 'stock/bin_edit.html', locals())


# 儲格編輯
@login_required
def bin_save(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == "edit":
            bin_code = request.POST.get('bin_code')
            if bin_code:
                bin = Bin.objects.get(bin_code=bin_code)

            form = BinEditForm(request.POST, instance=bin)
            if form.is_valid():
                tmp_form = form.save(commit=False)
                tmp_form.update_by = request.user
                tmp_form.save()
        elif action == "add":
            form = BinEditForm(request.POST)
            if form.is_valid():
                tmp_form = form.save(commit=False)
                tmp_form.update_by = request.user
                tmp_form.save()

        location_code = request.POST.get('location_code')
        location = Location.objects.get(location_code=location_code)
        storage_code = location.storage.storage_code
        bins = Bin.objects.filter(location=location).all()
        return render(request, 'stock/bin.html', locals())
    return render(request, 'stock/bin_edit.html', locals())


# 入庫作業
@transaction.atomic
@login_required
def stock_in(request):
    if request.method == 'POST':
        hidItem_list = request.POST.get('hidItem_list')
        if hidItem_list:
            items = json.loads(hidItem_list)

        apply_date = request.POST.get('apply_date')
        pr_no = request.POST.get('pr_no')
        desc = request.POST.get('desc')

        save_tag = transaction.savepoint()
        try:
            stock_in = StockInForm()
            YYYYMM = datetime.now().strftime("%Y%m")
            key = "SI"+YYYYMM
            stock_in.form_no = key + str(get_series_number(key, "入庫單")).zfill(3)
            stock_in.pr_no = pr_no
            stock_in.requester = request.user
            stock_in.apply_date = apply_date
            stock_in.reason = desc
            stock_in.create_by = request.user
            stock_in.save()

            for item in items:
                Do_Transaction(request, stock_in.form_no, 'STIN', item['item_code'], item['bin_code'], int(item['qty']), item['comment'])

        except Exception as e:
            transaction.savepoint_rollback(save_tag)
            print(e)

        return redirect(stock_in.get_absolute_url())
    form = StockInPForm()
    return render(request, 'stock/stock_in.html', locals())


@login_required
def stockin_detail(request, pk):
    try:
        form = StockInForm.objects.get(pk=pk)
        items = StockHistory.objects.filter(batch_no=pk)
    except StockInForm.DoesNotExist:
        raise Http404('Form does not exist')

    return render(request, 'stock/stockin_detail.html', locals())


# 出庫作業
@login_required
def stock_out(request):
    if request.method == 'POST':
        hidItem_list = request.POST.get('hidItem_list')
        if hidItem_list:
            items = json.loads(hidItem_list)

        apply_date = request.POST.get('apply_date')
        desc = request.POST.get('desc')

        save_tag = transaction.savepoint()
        try:
            stock_out = StockOutForm()
            YYYYMM = datetime.now().strftime("%Y%m")
            key = "SO"+YYYYMM
            stock_out.form_no = key + str(get_series_number(key, "入庫單")).zfill(3)
            stock_out.requester = request.user
            stock_out.apply_date = apply_date
            stock_out.reason = desc
            stock_out.create_by = request.user

            for item in items:
                qty = int(item['qty']) * -1
                result = Do_Transaction(request, stock_out.form_no, 'STOU', item['item_code'], item['bin_code'], qty, item['comment'])
                if result == "ERROR":
                    raise SyntaxError
            stock_out.save()
            return redirect(stock_out.get_absolute_url())
        except Exception as e:
            transaction.savepoint_rollback(save_tag)
            print(e)

    form = StockOutPForm()
    return render(request, 'stock/stock_out.html', locals())


@login_required
def stockout_detail(request, pk):
    try:
        form = StockOutForm.objects.get(pk=pk)
        items = StockHistory.objects.filter(batch_no=pk)
    except StockInForm.DoesNotExist:
        raise Http404('Form does not exist')

    return render(request, 'stock/stockout_detail.html', locals())


def item_search_popup(request):
    groups = request.user.groups.all()
    search_form = ItemSearchForm()
    search_form.fields["category"].queryset = ItemCategory.objects.filter(family__perm_group__in=groups).all()
    return render(request, 'stock/item_search_popup.html', locals())


def item_stock_search_popup(request):
    groups = request.user.groups.all()
    search_form = ItemSearchForm()
    search_form.fields["category"].queryset = ItemCategory.objects.filter(family__perm_group__in=groups).all()
    return render(request, 'stock/item_stock_search_popup.html', locals())


def bin_search_popup(request):
    search_form = BinSearchForm()
    return render(request, 'stock/bin_search_popup.html', locals())


def TypeAPI(request, category_id):
    type_data = ItemType.objects.filter(category_id=int(category_id)).values('id', 'type_name')
    type_list = []
    for data in type_data:
        type_list.append({'id': data['id'], 'type_name': data['type_name']})
    return JsonResponse(type_list, safe=False)


def LocationAPI(request, storage_code):
    loc_data = Location.objects.filter(storage__storage_code=storage_code).values('location_code', 'location_name')
    loc_list = []
    for data in loc_data:
        loc_list.append({'location_code': data['location_code'], 'location_name': data['location_name']})
    return JsonResponse(loc_list, safe=False)


#API類別
def StorageBinAPI(request):
    bin_list = []
    if request.method == 'POST':
        storage_code = request.POST.get('storage_code')
        location_code = request.POST.get('location_code')

        bin_data = Bin.objects.filter()

        if storage_code:
            bin_data = bin_data.filter(location__storage=storage_code).values('bin_code', 'bin_name')
        if location_code:
            bin_data = bin_data.filter(location=location_code).values('bin_code', 'bin_name')

        for data in bin_data:
            bin_list.append({'bin_code': data['bin_code'], 'bin_name': data['bin_name']})

    return JsonResponse(bin_list, safe=False)


# API Bin
def LocationBinAPI(request, location_code):
    location = Location.objects.get(location_code=location_code)
    bin_data = Bin.objects.filter(location=location).values('bin_code', 'bin_name')
    bin_list = []
    for data in bin_data:
        bin_list.append({'bin_code': data['bin_code'], 'bin_name': data['bin_name']})

    return JsonResponse(bin_list, safe = False)


#API類別
def ItemAPI(request):
    item_list = []
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        type_id = request.POST.get('type_id')
        keyword = request.POST.get('keyword')

        item_data = Item.objects.filter(is_stock=True)

        if category_id:
            item_type = ItemType.objects.filter(category_id=category_id)
            item_data = item_data.filter(item_type__in=item_type).values('item_code', 'spec', 'unit', 'item_pics__files')
        if type_id:
            item_data = item_data.filter(item_type_id=int(type_id)).values('item_code', 'spec', 'unit', 'item_pics__files')
        if keyword:
            query = Q(spec__icontains=keyword)
            item_data = item_data.filter(query).values('item_code', 'spec', 'unit', 'item_pics__files')

        for data in item_data:
            category = ItemCategory.objects.get(id=category_id)
            item_list.append({'item_code': data['item_code'], 'spec': data['spec'], 'unit': data['unit'],
                              'category': category.category_name, 'pic': data['item_pics__files']})

    return JsonResponse(item_list, safe=False)


#API類別
def StockItemAPI(request):
    item_list = []
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        type_id = request.POST.get('type_id')
        keyword = request.POST.get('keyword')

        item_data = Stock.objects.filter(qty__gt=0)

        if category_id:
            item_type = ItemType.objects.filter(category_id=category_id)
            item_data = item_data.filter(item__item_type__in=item_type).values('item__item_code', 'item__spec', 'item__unit', 'item__item_pics__files', 'qty', 'bin__bin_code', 'bin__bin_name')
        if type_id:
            item_data = item_data.filter(item__item_type_id=int(type_id)).values('item__item_code', 'item__spec', 'item__unit', 'item__item_pics__files', 'qty', 'bin__bin_code', 'bin__bin_name')
        if keyword:
            query = Q(item__spec__icontains=keyword)
            item_data = item_data.filter(query).values('item__item_code', 'item__spec', 'item__unit', 'item__item_pics__files', 'qty', 'bin__bin_code', 'bin__bin_name')

        for data in item_data:
            category = ItemCategory.objects.get(id=category_id)
            item_list.append({'item_code': data['item__item_code'], 'spec': data['item__spec'], 'unit': data['item__unit'],
                              'category': category.category_name, 'pic': data['item__item_pics__files'],
                              'qty': data['qty'], 'bin_code': data['bin__bin_code'], 'bin_name': data['bin__bin_name']})

    return JsonResponse(item_list, safe=False)


#API類別
def get_item_info(request):
    item_list = []
    if request.method == 'POST':
        try:
            item_code = request.POST.get('item_code')
            item = Item.objects.get(item_code=item_code)
            pic = item.item_pics.first().files.url if not item.item_pics else ''
            item_list.append({'category': item.item_type.type_name, 'item_code': item.item_code, 'spec': item.spec, 'unit': item.unit,
                              'pic': pic})
        except Item.DoesNotExist:
            raise Http404('Item does not exist')

        return JsonResponse(item_list, safe=False)


#API類別
def get_bin_info(request):
    bin_list = []
    if request.method == 'POST':
        try:
            bin_code = request.POST.get('bin_code')

            bin = Bin.objects.get(bin_code=bin_code)
            bin_list.append({'bin_code': bin.bin_code, 'bin_name': bin.bin_name})
        except Bin.DoesNotExist:
            raise Http404('Bin does not exist')

        return JsonResponse(bin_list, safe=False)


# 庫存查詢
@login_required
def stock_search(request):
    _storage = ""
    _location = ""
    _bin = ""
    _keyword = ""

    if 'storage' in request.session:
        _storage = request.session['storage']

    if 'location' in request.session:
        _location = request.session['location']

    if 'bin' in request.session:
        _bin = request.session['bin']

    if 'keyword' in request.session:
        _keyword = request.session['keyword']

    form = StockSearchForm(
        initial={'storage': _storage, 'location': _location, '_bin': _bin,
                 'keyword': _keyword})
    form.fields['storage'].queryset = Storage.objects.filter(enable=True)
    form.fields['location'].queryset = Location.objects.filter(storage__storage_code=_storage)
    form.fields['bin'].queryset = Bin.objects.filter(location__storage__storage_code=_storage)
    return render(request, 'stock/stock_search.html', locals())


# 庫存查詢
@login_required
def stock_search_action(request):
    page_number = 1
    _storage = ""
    _location = ""
    _bin = ""
    _keyword = ""
    stocks = Stock.objects.all()
    if request.method == 'POST':
        clean_session(request)
        _storage = request.POST.get('storage')
        _location = request.POST.get('location')
        _bin = request.POST.get('bin')
        _keyword = request.POST.get('keyword')

    if request.method == 'GET':
        if request.GET.get('page'):
            page_number = int(request.GET.get('page'))
        else:
            page_number = 1

        if 'storage' in request.session:
            _storage = request.session['storage']

        if 'location' in request.session:
            _location = request.session['location']

        if 'bin' in request.session:
            _bin = request.session['bin']

        if 'keyword' in request.session:
            _keyword = request.session['keyword']

    if _storage:
        request.session['all_storage'] = _storage
        stocks = stocks.filter(bin__location__storage__storage_code=_storage)

    if _location:
        request.session['location'] = _location
        stocks = stocks.filter(bin__location__location_code=_location)

    if _bin:
        request.session['bin'] = _bin
        stocks = stocks.filter(bin__bin_code=_bin)

    if _keyword:
        request.session['keyword'] = _keyword
        stocks = stocks.filter(Q(item__item_code__icontains=_keyword) | Q(item__desc__icontains=_keyword))

        stocks = stocks.order_by('item__item_code')

    results = list(stocks)
    page_obj = Paginator(results, 15)
    row_count = stocks.count()

    if page_number:
        page_results = page_obj.page(page_number)
    else:
        page_results = page_obj.page(1)

    form = StockSearchForm(initial={'storage': _storage, 'location': _location, 'bin': _bin, 'keyword': _keyword})
    form.fields['location'].queryset = Location.objects.filter(storage__storage_code=_storage)
    form.fields['bin'].queryset = Bin.objects.filter(location__storage__storage_code=_storage)
    return render(request, 'stock/stock_search.html', locals())


# 清除Session
def clean_session(request):
    """清除session"""
    if 'all_storage' in request.session:
        del request.session['all_storage']
    if 'location' in request.session:
        del request.session['location']
    if 'bin' in request.session:
        del request.session['bin']
    if 'keyword' in request.session:
        del request.session['keyword']


# 庫存查詢 Excel匯出 Queryset
def get_stock_queryset(request):
    _storage = ""
    _location = ""
    _bin = ""
    _keyword = ""
    stocks = Stock.objects.all()
    if request.method == 'POST':
        clean_session(request)
        _storage = request.POST.get('storage')
        _location = request.POST.get('location')
        _bin = request.POST.get('bin')
        _keyword = request.POST.get('keyword')

    if request.method == 'GET':
        if 'storage' in request.session:
            _storage = request.session['storage']

        if 'location' in request.session:
            _location = request.session['location']

        if 'bin' in request.session:
            _bin = request.session['bin']

        if 'keyword' in request.session:
            _keyword = request.session['keyword']

    if _storage:
        request.session['storage'] = _storage
        stocks = stocks.filter(bin__location__storage__storage_code=_storage)

    if _location:
        request.session['location'] = _location
        stocks = stocks.filter(bin__location__location_code=_location)

    if _bin:
        request.session['bin'] = _bin
        stocks = stocks.filter(bin__bin_code=_bin)

    if _keyword:
        request.session['keyword'] = _keyword
        stocks = stocks.filter(Q(item__item_code__icontains=_keyword) | Q(item__desc__icontains=_keyword))

        stocks = stocks.order_by('item__item_code')

    return stocks


# 庫存查詢 Excel匯出
@login_required
def stock_search_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="noah_inventory.xls"'.format()

    wb = xlwt.Workbook(encoding='utf-8')
    sheet_name = 'Noah Inventory'.format()
    ws = wb.add_sheet(sheet_name)
    ws.col(0).width = 256 * 20
    ws.col(1).width = 256 * 20
    ws.col(2).width = 256 * 20
    ws.col(3).width = 256 * 20
    ws.col(4).width = 256 * 20
    ws.col(5).width = 256 * 20
    ws.col(6).width = 256 * 20
    ws.col(7).width = 256 * 20
    ws.col(8).width = 256 * 20

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Storage', 'Location', '儲格', '料號', '物料說明', '庫存數量', '單位', '異動日期']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'yyyy/mm/dd'

    stocks = get_stock_queryset(request)

    for data in stocks:
        row_num += 1
        ws.write(row_num, 0, data.bin.location.storage.desc, font_style)
        ws.write(row_num, 1, data.bin.location.location_name, font_style)
        ws.write(row_num, 2, data.bin.bin_name, font_style)
        ws.write(row_num, 3, data.item.item_code, font_style)
        ws.write(row_num, 4, data.item.spec, font_style)
        ws.write(row_num, 5, data.qty, font_style)
        ws.write(row_num, 6, data.item.unit, font_style)
        ws.write(row_num, 7, data.update_at, date_format)

    wb.save(response)
    return response


# 料號異動紀錄
@login_required
def stock_history(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        start_date = request.POST.get('start_date')
        due_date = request.POST.get('due_date')

        if start_date:
            _start_date = datetime.strptime(start_date, '%Y-%m-%d')
        else:
            _start_date = datetime.now() - timedelta(days=30)

        if due_date:
            _due_date = datetime.strptime(due_date, '%Y-%m-%d') + timedelta(days=1)
        else:
            _due_date = datetime.now() + timedelta(days=1)

        hists = StockHistory.objects.filter(create_at__gte=_start_date, create_at__lte=_due_date)
        if keyword:
            hists = hists.filter(Q(item__item_code__icontains=keyword) | Q(item__spec__icontains=keyword))

        hists = hists.order_by('create_at')[:50]

        form = StockHistoryForm(initial={'keyword': keyword, 'start_date': start_date, 'due_date': due_date})
        return render(request, 'stock/stock_history.html', locals())

    form = StockHistoryForm()
    return render(request, 'stock/stock_history.html', locals())


# 近期異動紀錄
@login_required
def recent_history(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        start_date = request.POST.get('start_date')
        due_date = request.POST.get('due_date')

        if start_date:
            _start_date = datetime.strptime(start_date, '%Y-%m-%d')

        if due_date:
            _due_date = datetime.strptime(due_date, '%Y-%m-%d') + timedelta(days=1)

        hists = StockHistory.objects.filter(create_at__gte=_start_date, create_at__lte=_due_date)

        hists = hists.order_by('-create_at')
        form = RecentHistoryForm(initial={'start_date': start_date, 'due_date': due_date})
        return render(request, 'stock/recent_history.html', locals())

    form = RecentHistoryForm()
    return render(request, 'stock/recent_history.html', locals())


# 入庫單查詢
@login_required
def stockin_search(request):
    return render(request, 'stock/stockin_search.html', locals())


# 出庫單查詢
@login_required
def stockout_search(request):
    return render(request, 'stock/stockout_search.html', locals())
