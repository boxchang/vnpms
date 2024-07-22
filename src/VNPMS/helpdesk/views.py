from django.contrib.auth.decorators import login_required
from django.db import transaction
from helpdesk.forms import HelpdeskForm
from helpdesk.models import Helpdesk, Helpdesk_attachment, HelpdeskType
from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse
from django.core.paginator import Paginator


def get_data_index():
    obj = Helpdesk.objects.last()
    if obj:
        index = int(obj.help_no[4:]) + 1
    else:
        index = 1
    return index


def get_serial_num():
    no_last = "HELP" + str(get_data_index()).zfill(5)
    return no_last


@login_required
def index(request):
    helptypes = HelpdeskType.objects.all()
    return render(request, 'helpdesk/index.html', locals())


@login_required
def helpdesk_edit(request, pk):
    if pk:
        helpdesk = Helpdesk.objects.get(pk=pk)

    if request.method == 'POST':
        form = HelpdeskForm(request.POST, instance=helpdesk)
        if form.is_valid():
            with transaction.atomic():
                data = form.save(commit=False)
                data.save()

                if request.FILES.get('files1'):
                    request_file = Helpdesk_attachment(
                        files=request.FILES['files1'])
                    request_file.description = request.POST['description1']
                    request_file.helpdesk = data
                    request_file.save()
                if request.FILES.get('files2'):
                    request_file = Helpdesk_attachment(
                        files=request.FILES['files2'])
                    request_file.description = request.POST['description2']
                    request_file.helpdesk = data
                    request_file.save()

            return redirect(helpdesk.get_absolute_url())
    else:
        form = HelpdeskForm(instance=helpdesk)
    return render(request, 'helpdesk/helpdesk_edit.html', {'form': form, 'helpdesk': helpdesk})


@login_required
def helpdesk_delete(request, pk):
    try:
        with transaction.atomic():
            helpdesk = Helpdesk.objects.select_for_update().get(pk=pk)
            helpdesk.delete()
    except Exception as e:
        Exception('Unexpected error: {}'.format(e))

    return redirect(reverse('help_index'))


@login_required
def helpdesk_create(request):
    if request.method == 'POST':
        form = HelpdeskForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                tmp_form = form.save(commit=False)
                tmp_form.help_no = get_serial_num()  # 單編碼
                tmp_form.create_by = request.user
                tmp_form.update_by = request.user
                form.save()

                if request.FILES.get('files1'):
                    request_file = Helpdesk_attachment(
                        files=request.FILES['files1'])
                    request_file.description = request.POST['description1']
                    request_file.request = tmp_form
                    request_file.save()
                if request.FILES.get('files2'):
                    request_file = Helpdesk_attachment(
                        files=request.FILES['files2'])
                    request_file.description = request.POST['description2']
                    request_file.request = tmp_form
                    request_file.save()

            return redirect(tmp_form.get_absolute_url())
    else:
        form = HelpdeskForm()
    return render(request, 'helpdesk/helpdesk_edit.html', locals())


def helpdesk_detail(request, pk):
    FULL_URL_WITH_QUERY_STRINg = request.build_absolute_uri()
    FULL_URL = request.build_absolute_uri('?')
    ABSOLUTE_ROOT = request.build_absolute_uri('/')[:-1].strip("/")
    ABSOLUTE_ROOT_URL = request.build_absolute_uri('/').strip("/")

    try:
        data = Helpdesk.objects.get(pk=pk)
        files = Helpdesk_attachment.objects.filter(helpdesk=data).all()
        help_no = data.help_no

    except Helpdesk.DoesNotExist:
        raise Http404

    return render(request, 'helpdesk/helpdesk_detail.html', locals())


def helpdesk_guest(request, help_no):
    try:
        data = Helpdesk.objects.filter(help_no=help_no).first()
        help_no = data.help_no
        pk = data.pk
        files = Helpdesk_attachment.objects.filter(helpdesk=data).all()

    except Helpdesk.DoesNotExist:
        raise Http404

    return render(request, 'helpdesk/helpdesk_guest.html', locals())


@login_required
def helpdesk_file_delete(request, pk):
    q = request.GET.get('q')
    if q:
        helpdesk = Helpdesk.objects.get(pk=q)
    obj = Helpdesk_attachment.objects.get(pk=pk)
    if obj:
        obj.delete()
    return redirect(helpdesk.get_absolute_url())


def search(request):
    helptype_id = ""
    keywords = ""
    helptypes = HelpdeskType.objects.all()
    results = []

    if request.method == 'POST':
        keywords = request.POST.get('keywords')
        helptype_id = request.POST.get('help_type')

    if helptype_id:
        helptype_id = int(helptype_id)
        results = Helpdesk.objects.filter(help_type_id=helptype_id)
    else:
        results = Helpdesk.objects.all()

    if keywords:
        for keyword in keywords.split(' '):
            results = results.filter(
                Q(title__contains=keyword) | Q(desc__contains=keyword) | Q(help_no__contains=keyword))

    results = list(results.order_by('-update_at')[:50])
    page_obj = Paginator(results, 30)

    page_number = request.GET.get('page')
    if page_number:
        page_results = page_obj.page(page_number)
    else:
        page_results = page_obj.page(1)

    results_count = len(results)
    return render(request, 'helpdesk/search.html', locals())
