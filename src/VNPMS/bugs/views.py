from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms import HiddenInput
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from bases.models import Status, FormType
from bases.utils import save_data_index, get_serial_num, get_form_type, get_home_url
from bases.views import get_user_setting_pagenum
from bugs.forms import BugForm
from bugs.models import Bug, Bug_attachment
from projects.models import Project


@login_required
def bug_create(request):
    p = request.GET.get('p')  # 專案id
    project = Project.objects.get(pk=p)
    if request.method == 'POST':
        form = BugForm(request.POST)
        form.status = Status.objects.get(status_en='Wait')

        if form.is_valid():
            try:
                with transaction.atomic():
                    form_type = get_form_type('BUG')
                    tmp_form = form.save(commit=False)
                    tmp_form.project = project
                    tmp_form.bug_no = get_serial_num(p, form_type)  # Bug單編碼
                    tmp_form.create_by = request.user
                    tmp_form.update_by = request.user
                    tmp_form.save()
                    save_data_index(p, form_type)  # Save serial number after success

                    if request.FILES.get('files1'):
                        bug_file = Bug_attachment(files=request.FILES['files1'])
                        bug_file.description = request.POST['description1']
                        bug_file.bug = tmp_form
                        bug_file.save()
                    if request.FILES.get('files2'):
                        bug_file = Bug_attachment(files=request.FILES['files2'])
                        bug_file.description = request.POST['description2']
                        bug_file.bug = tmp_form
                        bug_file.save()
            except Exception as e:
                Exception('Unexpected error: {}'.format(e))

            return redirect(tmp_form.get_absolute_url())
    else:
        form = BugForm()
        form.fields['status'].widget = HiddenInput()

    return render(request, 'bugs/bug_edit.html', locals())



@login_required
def bug_edit(request, pk):
    if pk:
        bug = Bug.objects.get(pk=pk)

    if request.method == 'POST':
        form = BugForm(request.POST, instance=bug)
        if form.is_valid():
            try:
                with transaction.atomic():
                    tmp_form = form.save(commit=False)
                    if request.FILES.get('files1'):
                        bug_file = Bug_attachment(files=request.FILES['files1'])
                        bug_file.description = request.POST['description1']
                        bug_file.bug = tmp_form
                        bug_file.save()
                    if request.FILES.get('files2'):
                        bug_file = Bug_attachment(files=request.FILES['files2'])
                        bug_file.description = request.POST['description2']
                        bug_file.bug = tmp_form
                        bug_file.save()
                    tmp_form.save()
            except Exception as e:
                Exception('Unexpected error: {}'.format(e))
            return redirect(bug.get_absolute_url())
    else:
        form = BugForm(instance=bug)
    return render(request, 'bugs/bug_edit.html', locals())


@login_required
def bug_list(request):
    bugs = Bug.objects.all()

    return render(request, 'bugs/bug_list.html', locals())


@login_required
def bug_detail(request, pk):
    try:
        bug = Bug.objects.get(pk=pk)
        bug_no = bug.bug_no
        files = Bug_attachment.objects.filter(bug=bug).all()
        form_type = FormType.objects.filter(type='BUG').first()

    except Bug.DoesNotExist:
        raise Http404

    return render(request, 'bugs/bug_detail.html', locals())


@login_required
def bug_delete(request, pk):
    bug = Bug.objects.get(pk=pk)
    project_pk = bug.project.pk
    bug.delete()
    return redirect(reverse('request_page', kwargs={'pk': project_pk}))


@login_required
def bug_file_delete(request, pk):
    b = request.GET.get('b')
    if b:
        bug = Bug.objects.get(pk=b)
    obj = Bug_attachment.objects.get(pk=pk)
    if obj:
        obj.delete()
    return redirect(bug.get_absolute_url())


@login_required
def bug_page(request, pk):
    try:
        page_num = get_user_setting_pagenum(request)
        form_type = FormType.objects.filter(type='PROJECT').first()
        project_form = Project.objects.get(pk=pk)  # 專案詳細資料
    except Project.DoesNotExist:
        raise Http404
    return render(request, 'bugs/bug_page.html', locals())

