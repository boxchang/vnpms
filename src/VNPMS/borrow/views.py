from django.urls import reverse
from assets.models import AssetType, Asset, AssetStatus
from borrow.forms import BorrowForm, BorrowAdminForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from borrow.models import Borrow, BorrowItem


# bootstrap sub table
from users.models import Unit, CustomUser


def get_borrow_item_api(request, pk):
    _json = []
    items = BorrowItem.objects.filter(borrow=pk)
    for item in items:
        _json.append({"type_name": item.asset.type.type_name, "asset_no": item.asset.asset_no, "model": item.asset.model, "desc": item.asset.desc})
    return JsonResponse(_json, safe=False)


def find_asset_api(request):
    if request.method == 'POST':
        asset_no = request.POST.get('asset_no')
        asset = Asset.objects.get(asset_no=asset_no)
        name = "({status}){asset_no}　{model}　{desc}".format(status=asset.status, asset_no=asset.asset_no,
                                                            model=asset.model, desc=asset.desc)
        html = """[{{\"value\":\"{value}\", \"name\":\"{name}\"}}]""".format(value=asset_no, name=name)
    return JsonResponse(html, safe=False)


def get_asset_api(request):
    if request.method == 'POST':
        typeId = request.POST.get('typeId')
        assets = Asset.objects.filter(type=typeId, status__in=(9, 4))  # 狀態9可出借, 狀態4出借中
        html = ""

        for asset in assets:
            name = "({status}){asset_no}　{model}　{desc}".format(status=asset.status, asset_no=asset.asset_no, model=asset.model, desc=asset.desc)
            html += """<option value="{value}">{name}</option>""".format(value=asset.asset_no, name=name)
    return JsonResponse(html, safe=False)


def createDeptOption():
    rows = Unit.objects.all()
    html = "<option value="" selected>---------</option>"

    for row in rows:
        html += """<option value="{value}">{name}</option>""".format(value=row.id, name=row.unitName)
    return html


def createAssetTypeOption():
    status = AssetStatus.objects.get(status_name="可出借")
    assets = Asset.objects.filter(status=status).values("type").distinct()
    types = AssetType.objects.filter(id__in=assets)
    html = "<option value="" selected>---------</option>"

    for type in types:
        html += """<option value="{value}">{name}</option>""".format(value=type.id, name=type.type_name)
    return html


def record(request):
    return render(request, 'borrow/record.html', locals())


def apply(request):
    if request.method == 'POST':
        apply_dept = request.POST.get('apply_dept')
        apply_user = request.POST.get('apply_user')
        apply_date = request.POST.get('apply_date')
        expect_date = request.POST.get('expect_date')
        comment = request.POST.get('comment')
        borrow_list = request.POST.get('hidBorrowList')

        try:
            borrow = Borrow()
            borrow.app_dept = Unit.objects.get(id=apply_dept)
            borrow.app_user = CustomUser.objects.get(id=apply_user)
            borrow.comment = comment
            borrow.apply_date = apply_date
            borrow.expect_date = expect_date
            borrow.save()

            assets = borrow_list.split(",")
            for asset in assets:
                if asset:
                    item = BorrowItem()
                    item.borrow = borrow
                    asset = Asset.objects.get(asset_no=asset)
                    item.asset = asset
                    item.save()

                    asset.status = AssetStatus.objects.get(status_name='出借中')
                    asset.save()
        except Exception as e:
            print(e)

        return redirect(reverse('record'))

    form = BorrowForm()
    dept_options = createDeptOption()
    asset_type_options = createAssetTypeOption()
    return render(request, 'borrow/application.html', locals())


def update(request, pk):
    if request.method == 'POST':
        lend_date = request.POST.get('lend_date')
        return_date = request.POST.get('return_date')
        borrow = Borrow.objects.get(form_no=pk)
        items = BorrowItem.objects.filter(borrow=borrow)

        if borrow.finished is False:
            if lend_date and not return_date:
                borrow.lend_owner = request.user
                for item in items:
                    asset = Asset.objects.get(id=item.asset.id)
                    asset.status = AssetStatus.objects.get(id=4)  # 出借中
                    asset.save()

            if return_date:
                borrow.return_owner = request.user
                for item in items:
                    asset = Asset.objects.get(id=item.asset.id)
                    asset.status = AssetStatus.objects.get(id=9)  # 可出借
                    asset.save()

        form = BorrowAdminForm(request.POST, instance=borrow)
        if form.is_valid():
            tmp_form = form.save(commit=False)
            tmp_form.save()
    return render(request, 'borrow/record.html', locals())


def detail(request, form_no):
    borrow = Borrow.objects.get(form_no=form_no)
    items = borrow.borrow_item.all()
    admin_form = BorrowAdminForm(instance=borrow)
    return render(request, 'borrow/detail.html', locals())


def form_delete(request, form_no):
    borrow = Borrow.objects.get(form_no=form_no)
    for item in borrow.borrow_item.all():
        asset = Asset.objects.get(id=item.asset_id)
        asset.status = AssetStatus.objects.get(id=9)  # 可出借
        asset.save()
    borrow.delete()
    return render(request, 'borrow/record.html', locals())


def item_delete(request, form_no, asset_id):
    borrow = Borrow.objects.get(form_no=form_no)
    asset = Asset.objects.get(id=asset_id)
    asset.status = AssetStatus.objects.get(id=9)  # 可出借
    asset.save()

    item = BorrowItem.objects.get(asset=asset)
    item.delete()
    return render(request, 'borrow/record.html', locals())
