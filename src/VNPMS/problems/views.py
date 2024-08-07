from datetime import datetime, timedelta
import calendar
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum, Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from bases.utils import *
from bases.views import get_user_setting_pagenum
from problems.forms import ProblemForm, ProblemReplyForm, ProblemHistoryForm, ProblemChartForm
from problems.models import *
from django.core.serializers import serialize

@login_required
def problem_create(request):
    p = request.GET.get('p')  #單號id
    project = Project.objects.get(pk=p)
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                form_type = get_form_type('PROBLEM')
                tmp_form = form.save(commit=False)
                tmp_form.problem_no = get_serial_num(p, form_type)  # 問題單編碼
                tmp_form.project = project
                tmp_form.create_by = request.user
                tmp_form.update_by = request.user
                tmp_form.save()
                save_data_index(p, form_type)  # Save serial number after success

                if request.FILES.get('files1'):
                    problem_file = Problem_attachment(files=request.FILES['files1'])
                    problem_file.description = request.POST['description1']
                    problem_file.problem = tmp_form
                    problem_file.save()
                if request.FILES.get('files2'):
                    problem_file = Problem_attachment(files=request.FILES['files2'])
                    problem_file.description = request.POST['description2']
                    problem_file.problem = tmp_form
                    problem_file.save()

            return redirect(tmp_form.get_absolute_url())
    else:
        form = ProblemForm()

    return render(request, 'problems/problem_edit.html', locals())


@login_required
def problem_edit(request, pk):
    p = request.GET.get('p')  # 單號id
    project = Project.objects.get(pk=p)
    if pk:
        problem = Problem.objects.get(pk=pk)

    if request.method == 'POST':
        form = ProblemForm(request.POST, instance=problem)
        if form.is_valid():
            try:
                with transaction.atomic():
                    tmp_form = form.save(commit=False)
                    if request.FILES.get('files1'):
                        problem_file = Problem_attachment(files=request.FILES['files1'])
                        problem_file.description = request.POST['description1']
                        problem_file.problem = tmp_form
                        problem_file.save()
                    if request.FILES.get('files2'):
                        problem_file = Problem_attachment(files=request.FILES['files2'])
                        problem_file.description = request.POST['description2']
                        problem_file.problem = tmp_form
                        problem_file.save()
                    tmp_form.save()
            except Exception as e:
                Exception('Unexpected error: {}'.format(e))

            return redirect(tmp_form.get_absolute_url())
    else:
        form = ProblemForm(instance=problem)
    return render(request, 'problems/problem_edit.html', locals())


@login_required
def problem_list(request):
    problems = Problem.objects.all()

    return render(request, 'problems/problem_list.html', locals())


@login_required
def problem_detail(request, pk):
    problem = Problem.objects.get(pk=pk)
    files = Problem_attachment.objects.filter(problem=problem).all()
    problem_reply_form = ProblemReplyForm()
    problem_replys = Problem_reply.objects.filter(problem_no=problem).all()
    table_cnt = range(3-files.count())
    return render(request, 'problems/problem_detail.html', locals())


@login_required
def problem_delete(request, pk):
    problem = Problem.objects.get(pk=pk)
    project_pk = problem.project.pk
    replys = Problem_reply.objects.filter(problem_no=problem)
    problem.delete()
    replys.delete()
    return redirect(reverse('problem_page', kwargs={'pk': project_pk}))


@login_required
def reply_delete(request, pk):
    reply = Problem_reply.objects.get(pk=pk)
    reply.delete()
    return redirect(reverse('problem_detail', kwargs={'pk': reply.problem_no.pk}))


@login_required
def problem_file_delete(request, pk):
    p = request.GET.get('p')
    if p:
        problem = Problem.objects.get(pk=p)
    obj = Problem_attachment.objects.get(pk=pk)
    if obj:
        obj.delete()
    return redirect(problem.get_absolute_url())


@login_required
def problem_reply_create(request, pk):
    problem = Problem.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProblemReplyForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.problem_no = problem
            data.create_by = request.user
            data.update_by = request.user
            data.save()

    return redirect(problem.get_absolute_url())


@login_required
def problem_page(request, pk):
    try:
        page_num = get_user_setting_pagenum(request)
        form_type = FormType.objects.filter(type='PROJECT').first()
        project_form = Project.objects.get(pk=pk)  # 專案詳細資料
    except Project.DoesNotExist:
        raise Http404
    return render(request, 'problems/problem_page.html', locals())


@login_required
def problem_history(request):
    p = request.GET.get('p')  # 專案id
    project = Project.objects.get(pk=p)
    if request.method == 'POST':
        _status = request.POST['status']
        _problem_type = request.POST['problem_type']
        _start_date = str(request.POST['start_date']).replace('/', '-')
        _due_date = str(request.POST['due_date']).replace('/', '-')

        _due_date = datetime.datetime.strptime(_due_date, "%Y-%m-%d")
        _due_date = _due_date + timedelta(days=1)
        _due_date = _due_date.strftime("%Y-%m-%d")

        problems = Problem.objects.filter(project=project)
        if _status:
            problems = problems.filter(problem_status=_status)

        if _start_date and _due_date:
            problems = problems.filter(create_at__gte=_start_date, create_at__lte=_due_date)

        if _problem_type:
            problems = problems.filter(problem_type=_problem_type)

        form = ProblemHistoryForm(request.POST)
    else:
        form = ProblemHistoryForm()
    return render(request, 'problems/problem_history.html', locals())


@login_required
def problem_chart(request):
    p = request.GET.get('p')  # 單號id
    project = Project.objects.get(pk=p)
    form = ProblemChartForm()
    return render(request, 'problems/problem_chart.html', locals())


@login_required
def problem_chart_grid_api(request):
    if request.method == 'POST':
        problem_type = request.POST['label']
        start_date = request.POST['start_date']

        start_date = datetime.datetime.strptime(start_date, "%Y-%m")
        _start_date = datetime.datetime(start_date.year, start_date.month, 1)
        _last_date = datetime.datetime(start_date.year, start_date.month,
                                       calendar.monthrange(start_date.year, start_date.month)[1]) + timedelta(days=1)
        problem_type = ProblemType.objects.get(type_name=problem_type)
        results = Problem.objects.filter(create_at__gte=_start_date, create_at__lte=_last_date, problem_type=problem_type).order_by('-problem_datetime')

        results_list = list(results.values())

        response = {
            "page": 1,
            "total": 1,
            "records": len(results_list),
            "rows": results_list
        }

        return JsonResponse(response, safe=False)


@login_required
def problem_chart_api(request):
    if request.method == 'POST':
        status = request.POST['status']
        start_date = request.POST['start_date']
        results= {}
        summary = Problem.objects.all()

        if start_date:
            start_date = datetime.datetime.strptime(start_date, "%Y-%m")
            _start_date = datetime.datetime(start_date.year, start_date.month, 1)
            _last_date = datetime.datetime(start_date.year, start_date.month, calendar.monthrange(start_date.year, start_date.month)[1]) + timedelta(days=1)

            summary = summary.filter(create_at__gte=_start_date, create_at__lte=_last_date)

        if status:
            summary = summary.filter(problem_status=status)

        summary = summary.values('problem_type').annotate(total=Count('problem_type')).order_by('-total')
        labels = []
        values = []
        for data in summary:
            labels.append(ProblemType.objects.get(pk=data['problem_type']).type_name)
            values.append(data['total'])
        results['labels'] = labels
        results['values'] = values
        return JsonResponse(results, safe=False)
