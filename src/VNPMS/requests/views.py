import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from bases.utils import *
from bases.views import get_user_setting_pagenum
from requests.forms import *
from requests.utils import *
from tests.models import Request_test


@login_required
def request_receive(request):
    r = request.GET.get('r')  # 專案id
    data = Request.objects.get(pk=r)

    if request.method == 'POST':
        form = RequestReceiveForm(request.POST, instance=data)

        if form.is_valid():
            status = Status.objects.filter(status_en="On-Going").first()
            tmp_form = form.save(commit=False)
            tmp_form.owner = request.user
            tmp_form.status = status
            tmp_form.save()
            return redirect(tmp_form.get_absolute_url())
    else:
        form = RequestReceiveForm(instance=data)
    return render(request, 'requests/request_receive.html', locals())

@login_required
def request_reply(request, pk):
    if request.method == 'POST':
        form = RequestReplyForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                tmp_form = form.save(commit=False)
                req = Request.objects.get(pk=pk)
                tmp_form.request = req
                tmp_form.create_by = request.user
                form.save()
            return redirect(req.get_absolute_url())


@login_required
def request_create(request):
    p = request.GET.get('p')  # 專案id
    t = request.GET.get('t')  # 單號類型
    r = request.GET.get('r')  # 需求id
    project = Project.objects.get(pk=p)
    if request.method == 'POST':
        #  STATUS/PROJECT/REQUEST由系統自動給
        form = RequestForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                form_type = get_form_type('REQUEST')
                tmp_form = form.save(commit=False)
                tmp_form.project = project
                if r:
                    tmp_form.belong_to = Request.objects.get(pk=r)
                tmp_form.request_no = get_serial_num(p, form_type)  # 需求單編碼
                tmp_form.create_by = request.user
                tmp_form.update_by = request.user
                form.save()
                # Save serial number after success
                save_data_index(p, form_type)

                if request.FILES.get('files1'):
                    request_file = Request_attachment(
                        files=request.FILES['files1'])
                    request_file.description = request.POST['description1']
                    request_file.request = tmp_form
                    request_file.save()
                if request.FILES.get('files2'):
                    request_file = Request_attachment(
                        files=request.FILES['files2'])
                    request_file.description = request.POST['description2']
                    request_file.request = tmp_form
                    request_file.save()

            return redirect(tmp_form.get_absolute_url())
    else:
        form = RequestForm()
    return render(request, 'requests/request_edit.html', locals())


@login_required
def request_edit(request, pk):
    if pk:
        require = Request.objects.get(pk=pk)
        project = require.project

    if request.method == 'POST':
        form = RequestForm(request.POST, instance=require)
        if form.is_valid():
            with transaction.atomic():
                data = form.save(commit=False)
                data.process_rate = data.status.process_rate
                data.save()

                if require.belong_to:
                    update_process_rate(require.belong_to)  # 更新父層的進度

                if request.FILES.get('files1'):
                    request_file = Request_attachment(
                        files=request.FILES['files1'])
                    request_file.description = request.POST['description1']
                    request_file.request = data
                    request_file.save()
                if request.FILES.get('files2'):
                    request_file = Request_attachment(
                        files=request.FILES['files2'])
                    request_file.description = request.POST['description2']
                    request_file.request = data
                    request_file.save()

            return redirect(require.get_absolute_url())
    else:
        form = RequestForm(instance=require)
    return render(request, 'requests/request_edit.html', locals())

@login_required
def reply_edit(request, pk):
    if pk:
        reply = Request_reply.objects.get(pk=pk)

    if request.method == 'POST':
        form = RequestReplyForm(request.POST, instance=reply)
        if form.is_valid():
            with transaction.atomic():
                req = Request.objects.get(pk=reply.request.pk)
                data = form.save(commit=False)
                data.save()
            return redirect(req.get_absolute_url())
    else:
        form = RequestReplyForm(instance=reply)
    return render(request, 'requests/reply_edit.html', {'form': form, 'reply': reply})

@login_required
def request_list(request):
    requests = cal_sub_requests(Request.objects.all())
    requests = cal_problems(requests)

    return render(request, 'requests/request_list.html', {'requests': requests})


@login_required
def request_history(request):
    p = request.GET.get('p')  # 專案id
    project = Project.objects.get(pk=p)
    if request.method == 'POST':
        _status = request.POST['status']
        _start_date = str(request.POST['start_date']).replace('/', '-')
        _due_date = str(request.POST['due_date']).replace('/', '-')
        requires = Request.objects.filter(project=project)
        if _status:
            requires = requires.filter(status=_status)

        if _start_date and _due_date:
            requires = requires.filter(create_at__gte=_start_date, create_at__lte=_due_date)

        form = RequestHistoryForm(request.POST)
    else:
        form = RequestHistoryForm()
    return render(request, 'requests/request_history.html', locals())


@login_required
def request_detail(request, pk):
    FULL_URL_WITH_QUERY_STRINg = request.build_absolute_uri()
    FULL_URL = request.build_absolute_uri('?')
    ABSOLUTE_ROOT = request.build_absolute_uri('/')[:-1].strip("/")
    ABSOLUTE_ROOT_URL = request.build_absolute_uri('/').strip("/")

    try:
        data = Request.objects.get(pk=pk)
        status_html = get_status_dropdown(data)
        project = data.project.pk
        request_no = data.request_no
        project = data.project.pk
        files = Request_attachment.objects.filter(request=data).all()

        bread = []
        father = data.belong_to
        while father:
            bread.insert(0, father)
            father = father.belong_to
        # 子需求表格
        form = RequestForm(project, initial={'belong_to': pk})

        # Reply
        reply_form = RequestReplyForm()
        replies = Request_reply.objects.filter(request=data).all()

        # 子需求
        sub_requests = cal_sub_requests(Request.objects.filter(belong_to=data))

        form_type = FormType.objects.filter(type='REQUEST').first()

        test = Request_test.objects.filter(request=data).first()
        if test:
            test_no = test.pk

    except Request.DoesNotExist:
        raise Http404

    return render(request, 'requests/request_detail.html', locals())


def request_guest(request, no):
    try:
        data = Request.objects.filter(request_no=no).first()
        request_no = data.request_no
        pk = data.pk

        files = Request_attachment.objects.filter(request=data).all()

        form_type = FormType.objects.filter(type='REQUEST').first()

        test = Request_test.objects.filter(request=data).first()
        if test:
            test_no = test.pk

        # Reply
        reply_form = RequestReplyForm()
        replies = Request_reply.objects.filter(request=data).all()

    except Request.DoesNotExist:
        raise Http404

    return render(request, 'requests/request_guest.html', locals())


@login_required
def request_delete(request, pk):

    try:
        with transaction.atomic():
            require = Request.objects.select_for_update().get(pk=pk)
            project_pk = require.project.pk
            request_delete_all(require)
    except Exception as e:
        Exception('Unexpected error: {}'.format(e))

    return redirect(reverse('request_page', kwargs={'pk': project_pk}))

@login_required
def reply_delete(request, pk):
    try:
        with transaction.atomic():
            obj = Request_reply.objects.select_for_update().get(pk=pk)
            require = Request.objects.get(pk=obj.request.pk)
            obj.delete()
    except Exception as e:
        Exception('Unexpected error: {}'.format(e))

    return redirect(require.get_absolute_url())


@login_required
def request_file_delete(request, pk):
    q = request.GET.get('q')
    if q:
        require = Request.objects.get(pk=q)
    obj = Request_attachment.objects.get(pk=pk)
    if obj:
        obj.delete()
    return redirect(require.get_absolute_url())


# 清除相關所有子需求
def request_delete_all(obj):
    sub_requires = Request.objects.select_for_update().filter(belong_to=obj)
    if sub_requires.count() > 0:
        for obj2 in sub_requires:
            request_delete_all(obj2)
    obj.delete()


def change_status(request):
    if request.POST:
        request_id = request.POST.get('request_id')
        status_id = request.POST.get('status_id')

        status = Status.objects.get(pk=status_id)
        obj = Request.objects.get(pk=request_id)
        obj.status = status
        if status.status_en == "Finished":
            obj.actual_date = datetime.now()
        obj.save()

        return redirect(obj.get_absolute_url())
    return redirect(get_home_url(request))


# [AJAX]依參數回拋需求JSON格式
def get_request(request):
    result = ""

    if request.GET.get('p'):
        # 為了取得父需求的PK值
        father_req = Request.objects.filter(
            request_no=str(request.GET.get('p')))
        objs = Request.objects.filter(belong_to=father_req.first().pk)
    else:
        objs = Request.objects.filter(belong_to__isnull=True)

    if objs:

        for obj in objs:
            tmp = ""
            tmp += "num: '{num}'" \
                   ",title: '{title}'," \
                   "level: '{level}'," \
                   "status: '{status}'," \
                   "belongto: '{belongto}'," \
                   "starttime: '{starttime}'," \
                   "finishtime: '{finishtime}'," \
                   "rate: '100%'," \
                   "subrequire:'(1/2)'," \
                   "question:'-'"
            tmp = tmp.format(num=obj.request_no,
                             title=obj.title,
                             level=obj.level,
                             status=obj.status,
                             belongto=obj.belong_to,
                             starttime=obj.start_date,
                             finishtime=obj.due_date)
            result += "{" + tmp + "},"
        result = '[ {0} ]'.format(result[:-1])  # 去尾

    return JsonResponse(result, safe=False)


def request_index(request, pk):
    requestindex = Request.objects.get(pk=pk)

    requests = Request.objects.filter(belong_to=pk)           # 從資料庫撈子需求

    request_table = json.dumps(requestTable(requests))        # 建立子需求Table

    problems = Problem.objects.filter(belong_to=pk)

    problem_table = json.dumps(problemTable(problems))

    return render(request, 'requests/request.html', locals())


def requestTable(requests):
    request_json = []
    for request in requests:

        rr = {}
        rr['pk'] = request.pk
        rr['num'] = str(request.request_no)
        rr['title'] = str(request.title)
        rr['level'] = str(request.level)
        rr['status'] = str(request.status)
        rr['owner'] = str(request.owner)
        rr['starttime'] = str(request.start_date)
        rr['finishtime'] = str(request.due_date)
        rr['rate'] = request.process
        rr['subrequire'] = '-'
        # rr['question'] = '-'

        request_json.append(rr)
    return request_json


def problemTable(problems):
    problem_json = []
    for problem in problems:
        reply = replies(problem.pk)
        rr = {}
        rr['pk'] = problem.pk
        rr['num'] = str(problem.problem_no)
        rr['title'] = str(problem.title)
        rr['rpl_cnt'] = str(reply.count())
        rr['creater'] = str(problem.create_by)
        rr['builttime'] = str(problem.create_at)
        try:
            rr['update_by'] = str(reply[0].update_by)
            rr['update_at'] = str(reply[0].update_at)
        except:
            rr['update_by'] = '-'
            rr['update_at'] = '-'
        problem_json.append(rr)
    return problem_json


def replies(pk):
    problem_replies = Problem_reply.objects.filter(
        problem_no=pk).order_by('-update_at')
    return problem_replies


@login_required
def request_page(request, pk):
    try:
        page_num = get_user_setting_pagenum(request)
        form_type = FormType.objects.filter(type='PROJECT').first()
        project_form = Project.objects.get(pk=pk)  # 專案詳細資料
    except Project.DoesNotExist:
        raise Http404
    return render(request, 'requests/request_page.html', locals())
