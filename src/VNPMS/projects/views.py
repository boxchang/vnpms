import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from bases.models import FormType, Status
from bases.utils import get_home_url
from bugs.models import Bug
from problems.models import Problem
from projects.forms import ProjectForm, ProjectSettingForm
from projects.models import Project, Project_setting
from requests.models import Request


# def index(request):
#     requests = Request.objects.all()
#     status = Status.objects.all()
#
#     return render(request, 'projects/index.html', locals())
from users.forms import CustomUserChangeForm
from users.models import CustomUser


def index(request):
    if request.user.pk:
        # 若沒有專案，就導向專案新增
        proj_count = Project.objects.all().count()
        if proj_count == 0:
            return redirect(reverse('project_create'))

        # 若沒有設定專案，就導向專案設定
        obj = CustomUser.objects.get(pk=request.user.pk)
        if obj.setting_user.first():
            return redirect(reverse('pms_home'))
        else:
            return redirect(reverse('project_setting'))
    else:
        return redirect(reverse('login'))


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.create_by = request.user
            project.update_by = request.user
            project.save()
            return redirect(reverse("project_setting"))
    else:
        form = ProjectForm()
    return render(request, 'projects/project_edit.html', locals())


@login_required
def project_edit(request, pk):
    if pk:
        project = Project.objects.get(pk=pk)
        form = ProjectForm(instance=project)

    if request.method == 'POST':

        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()  # 在預設情況下，model form 的 save 會自動幫你呼叫 model 的 save, commit是關掉
            # if request.user.is_authenticated():
            #     pass
            # project.owner = request.user
            # project.save()
            return redirect(project.get_absolute_url())

    return render(request, 'projects/project_edit.html', {'form': form, 'project': project})


def project_delete(request, pk):
    try:
        with transaction.atomic():
            project = Project.objects.select_for_update().get(
                pk=pk)  # select_for_update鎖表，執行完後才會釋放
            project.delete()
    except Exception as e:
        Exception('Unexpected error: {}'.format(e))

    return redirect(get_home_url(request))


@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})


@login_required
def project_manage(request, pk):  # 回傳projects/manage的頁面主體資料
    try:
        page_num = 5
        form_type = FormType.objects.filter(type='PROJECT').first()
        # 取得使用者專案設定
        if request.user.setting_user:
            project_setting = request.user.setting_user.first()
            page_num = project_setting.page_number

        project_form = Project.objects.get(pk=pk)  # 專案詳細資料
    except Project.DoesNotExist:
        raise Http404

    return render(request, 'projects/project_manage.html', locals())


@login_required
def project_setting(request):
    try:
        data = Project_setting.objects.filter(user=request.user).first()
    except Project_setting.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = ProjectSettingForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user

            if request.FILES.get('shot'):
                user = CustomUser.objects.get(pk=request.user.pk)
                name, extension = os.path.splitext(
                    request.FILES.get('shot')._name)
                # 先刪除舊的
                fullname = os.path.join(
                    settings.MEDIA_ROOT, 'uploads/profile', request.user.username + extension)
                if os.path.exists(fullname):
                    os.remove(fullname)
                # 換檔案名稱
                user.shot = request.FILES['shot']
                user.shot.name = request.user.username + extension
                user.save()

            obj.save()
            form.save_m2m()

            default_pk = obj.default.pk
            return redirect(reverse('request_page', kwargs={'pk': default_pk}))
        else:
            print(form.errors)
    else:
        if data:
            form = ProjectSettingForm(instance=data)
        else:
            form = ProjectSettingForm()

    return render(request, 'projects/project_setting.html', locals())


@login_required
def search(request):
    if request.method == 'POST':
        keywords = request.POST.get('keywords')

        results = []

        if keywords:
            for keyword in keywords.split(' '):
                r_results = list(Request.objects.extra(select={'no': 'request_no'}).filter(
                    Q(title__contains=keyword) | Q(desc__contains=keyword) | Q(request_no__contains=keyword)))
                for r_result in r_results:
                    r_result.type = 'R'
                results += r_results
            for keyword in keywords.split(' '):
                p_results = list(Problem.objects.extra(select={'no': 'problem_no'}).filter(
                    Q(title__contains=keyword) | Q(desc__contains=keyword) | Q(problem_no__contains=keyword)))
                for p_result in p_results:
                    p_result.type = 'P'
                results += p_results
            for keyword in keywords.split(' '):
                b_results = list(Bug.objects.extra(select={'no': 'bug_no'}).filter(
                    Q(title__contains=keyword) | Q(desc__contains=keyword) | Q(bug_no__contains=keyword)))
                for b_result in b_results:
                    b_result.type = 'B'
                results += b_results
        results_count = len(results)
    return render(request, 'projects/search.html', locals())


@login_required
def pms_home(request):

    # 在index就有判斷使用者設定，理論上這邊一定會有值
    obj = CustomUser.objects.get(pk=request.user.pk)
    if obj.setting_user.first():
        pk = obj.setting_user.first().default.pk
    else:
        return redirect(reverse('project_setting'))
    assert obj != None, u'user setting can\'t get at bases\\views.py'

    # project_setting = Project_setting.objects.user.filter().first()
    project_setting = Project_setting.objects.get(user=obj)
    projects = project_setting.project.all()

    problems = Problem.objects.filter(project__in=projects).order_by('-create_at')[:40]
    status = Status.objects.filter(status_en__in=['Wait', 'On-Going', 'Done', 'Pending'])
    requests = Request.objects.filter(project__in=projects, status__in=status).order_by('-create_at')[:40]

    return render(request, 'projects/homepage.html', locals())
