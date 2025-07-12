from datetime import datetime, timedelta
import calendar
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum, Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from bases.utils import *
from bases.models import Status
from bases.views import get_user_setting_pagenum
from problems.forms import ProblemForm, ProblemReplyForm, ProblemHistoryForm, ProblemChartForm
from problems.models import *
from users.models import Group, Member, Unit, Plant, UserType
from projects.models import Project_setting
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.utils.dateparse import parse_date
import json
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from collections import defaultdict
import base64
# from bs4 import BeautifulSoup
import uuid
from django.core import serializers
from django.core.serializers import serialize
from django.http import HttpResponse
from bases.utils import send_wecom_message


@login_required
def problem_receive(request):
    r = request.GET.get('r')  # 專案id
    problem = Problem.objects.get(pk=r)

    problem.owner = request.user
    problem.problem_status = Status.objects.get(status_en='On-Going')
    problem.save()

    return redirect('problem_detail', pk=problem.pk)


@login_required
def problem_create(request):
    p = request.GET.get('p')  #單號id
    user = CustomUser.objects.get(pk=request.user.pk)
    project = Project.objects.get(pk=p)
    if request.method == 'POST':
        form = ProblemForm(request.POST, project=project, user=user)
        if form.is_valid():
            with transaction.atomic():
                form_type = get_form_type('PROBLEM')
                tmp_form = form.save(commit=False)
                tmp_form.problem_no = get_serial_num(p, form_type)  # 問題單編碼
                tmp_form.project = project

                # Safely handle owner assignment
                owner_id = request.POST.get('owner')
                if owner_id:  # Only try to get user if owner_id exists and is not empty
                    try:
                        tmp_form.owner = CustomUser.objects.get(pk=owner_id)
                    except (CustomUser.DoesNotExist, ValueError):
                        # Handle invalid user ID (log error if needed)
                        tmp_form.owner = None
                else:
                    tmp_form.owner = None

                # Safely handle problem status
                problem_status_id = request.POST.get('problem_status')
                # Set problem status is "Wait For Assign" by default
                # if problem_status_id:  # Only try to get status if status_id exists and is not empty
                #     try:
                #         tmp_form.problem_status_id = problem_status_id
                #     except (ProblemType.DoesNotExist, ValueError):
                #         # Handle invalid status ID (log error if needed)
                #         tmp_form.problem_status_id = Status.objects.get(status_en="Wait For Assign")
                # else:
                #     tmp_form.problem_status_id = Status.objects.get(status_en="Wait For Assign")

                # # Safely handle problem type
                # problem_type_id = request.POST.get('problem_type')
                # if problem_type_id:  # Only try to get user if owner_id exists and is not empty
                #     try:
                #         tmp_form.problem_type = ProblemType.objects.get(pk=problem_type_id)
                #     except (ProblemType.DoesNotExist, ValueError):
                #         # Handle invalid user ID (log error if needed)
                #         tmp_form.problem_type = None
                # else:
                #     tmp_form.owner = None

                if request.user.user_type.type_name == "Normal":
                    tmp_form.owner = request.user
                    tmp_form.problem_status = Status.objects.get(status_en="On-Going")
                else:
                    tmp_form.problem_status = Status.objects.get(status_en="Wait For Assign")

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

                # Send WeCom message
                issue_owner_line = f"**Issue Owner**: {tmp_form.owner.username}  \n" if tmp_form.owner_id else ""
                msg = f"""### ⚠️🛠️ [NEW PROBLEM]
                **Problem number**: {tmp_form.problem_no}
                **Problem**: {tmp_form.title}
                **Requester**: {tmp_form.requester}
                **Plant**: {tmp_form.plant.plant_name}
                **Department**: {tmp_form.dept.unitName}
                **Status**: *{tmp_form.problem_status.status_en}*
                {issue_owner_line}\n👉 [Check The Problem Here]({request.build_absolute_uri(tmp_form.get_absolute_url())})
                """
                send_wecom_message(msg)

            return redirect(tmp_form.get_absolute_url())
    else:
        form = ProblemForm(project=project, user=user)

    return render(request, 'problems/problem_edit.html', locals())


def load_depts(request):
    plant_id = request.GET.get('plant_id')
    depts = Unit.objects.filter(plant_id=plant_id).values('id', 'unitName')
    return JsonResponse({'depts': list(depts)})


@login_required
def problem_edit(request, pk):
    p = request.GET.get('p')  # 單號id
    user = CustomUser.objects.get(pk=request.user.pk)
    project = Project.objects.get(pk=p)

    # Ensure group exists
    group_admin_user = CustomUser.objects.get(username='box_chang')

    group, created = Group.objects.get_or_create(
        group_name='Issue Owner',
        group_description='This group includes all IT department members responsible for handling problems.',
        defaults={'create_by': group_admin_user, 'update_by': group_admin_user}
    )

    if not Member.objects.filter(member=group_admin_user, group=group).exists():
        Member.objects.create(
            member=group_admin_user,
            group=group,
            isJoin=True,
            create_by=request.user
        )

    group_users = CustomUser.objects.filter(
        pk__in=Member.objects.filter(group=group).values_list('member_id', flat=True)
    ).distinct()

    if pk:
        problem = Problem.objects.get(pk=pk)
        # if problem.dept:
        #     unit = Unit.objects.get(pk=problem.dept)
        #     problem.dept = unit.unitName
        # if problem.plant:
        #     plant = Plant.objects.get(pk=problem.plant)
        #     problem.plant = plant.plant_code

    if request.method == 'POST':
        form = ProblemForm(request.POST, instance=problem, project=project, user=user, members=group_users)
        if form.is_valid():
            try:
                with transaction.atomic():
                    tmp_form = form.save(commit=False)
                    selected_owner = form.cleaned_data.get('owner')
                    if selected_owner:
                        tmp_form.owner = selected_owner
                        if tmp_form.problem_status.status_en == 'Wait For Assign':
                            on_going_status = Status.objects.get(status_en='On-Going')
                            tmp_form.problem_status = on_going_status
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
        form = ProblemForm(instance=problem, project=project, user=user, members=group_users)
    return render(request, 'problems/problem_edit.html', locals())


@login_required
def problem_list(request):
    problems = Problem.objects.all()

    return render(request, 'problems/problem_list.html', locals())


@login_required
def problem_detail(request, pk):
    problem = Problem.objects.get(pk=pk)
    m = request.user.user_type.type_name
    if str(problem.dept).isdigit():
        try:
            unit = Unit.objects.get(pk=problem.dept)
            problem.dept = unit.unitName
        except Unit.DoesNotExist:
            pass

    if str(problem.plant).isdigit():
        try:
            plant = Plant.objects.get(pk=problem.plant)
            problem.plant = plant.plant_code
        except Unit.DoesNotExist:
            pass

    status_html = get_status_dropdown(o_id=problem.id, o_status=problem.problem_status)
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
        assigning_users = CustomUser.objects.all().values('id', 'username')
        user = CustomUser.objects.get(pk=request.user.pk)

        group_ids = Member.objects.filter(member_id=request.user.pk).values_list('group_id', flat=True)

        group_users = list(CustomUser.objects.filter(
            pk__in=Member.objects.filter(group_id__in=group_ids).values_list('member_id', flat=True)
        ).distinct().values('id', 'username'))

        # groups = Group.objects.prefetch_related('member_set__member')
        # group_data = [
        #     {
        #         'group_name': g.group_name,
        #         'members': [
        #             {'id': m.member.id, 'username': m.member.username}
        #             for m in g.member_set.all() if hasattr(m, 'member')
        #         ]
        #     }
        #     for g in groups
        # ]
        # group_data_json = json.dumps(group_data)

        group_users_json = json.dumps(list(group_users))
    except Project.DoesNotExist:
        raise Http404
    return render(request, 'problems/problem_page.html', {
        **locals(),
        'assigning_users': list(assigning_users),
        'group_users_json': group_users_json
    })


@login_required
def problem_history(request):
    p = request.GET.get('p')  # 專案id
    project = Project.objects.get(pk=p)
    if request.method == 'POST':
        _problem_type = request.POST['problem_type']
        _owner = request.POST['owner']
        _status = request.POST['problem_status']
        _start_date = str(request.POST['start_date']).replace('/', '-')
        _due_date = str(request.POST['due_date']).replace('/', '-')
        _due_date = datetime.datetime.strptime(_due_date, "%Y-%m-%d")
        _due_date = _due_date + timedelta(days=1)
        _due_date = _due_date.strftime("%Y-%m-%d")

        problems = Problem.objects.filter(project=project)

        if _start_date and _due_date:
            problems = problems.filter(create_at__gte=_start_date, create_at__lte=_due_date)

        if _problem_type:
            problems = problems.filter(problem_type=_problem_type)

        if _owner:
            problems = problems.filter(owner=_owner)

        if _status:
            problems = problems.filter(problem_status=_status)

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
        project = request.POST['project']
        project = Project.objects.get(pk=project)

        start_date = datetime.datetime.strptime(start_date, "%Y-%m")
        _start_date = datetime.datetime(start_date.year, start_date.month, 1)
        _last_date = datetime.datetime(start_date.year, start_date.month,
                                       calendar.monthrange(start_date.year, start_date.month)[1]) + timedelta(days=1)
        problem_type = ProblemType.objects.filter(belong_to=project.belong_to, type_name=problem_type).first()
        results = Problem.objects.filter(create_at__gte=_start_date, create_at__lte=_last_date, problem_type=problem_type).order_by('-problem_datetime')

        results_list = list(results.values('id', 'problem_datetime', 'plant__plant_code', 'title', 'requester'))

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
        project = request.POST['project']
        project = Project.objects.get(pk=project)
        results = {}
        summary = Problem.objects.filter(project=project)

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
            if data['problem_type']:
                labels.append(ProblemType.objects.filter(belong_to=project.belong_to, pk=data['problem_type']).first().type_name)
                values.append(data['total'])
        results['labels'] = labels
        results['values'] = values
        return JsonResponse(results, safe=False)


@login_required
def change_status(request):
    if request.POST:
        problem_id = request.POST.get('o_id')
        status_id = request.POST.get('status_id')

        status = Status.objects.get(pk=status_id)
        obj = Problem.objects.get(pk=problem_id)
        obj.problem_status = status
        if status.status_en == "Done":
            obj.finish_datetime = datetime.datetime.now()
        obj.save()

        return redirect(obj.get_absolute_url())
    return redirect(get_home_url(request))


@login_required
@require_POST
def assign_problem(request, problem_id):
    try:
        problem = Problem.objects.get(pk=problem_id)
        assign_to_id = request.POST.get('assign_to')

        # Validate assign_to_id is not 0 (default "Please assign" option)
        if assign_to_id == '0':
            return JsonResponse({'status': 'error', 'message': 'Please select a valid user'}, status=400)

        assign_to = CustomUser.objects.get(pk=assign_to_id)
        status = Status.objects.get(status_en="On-Going")
        problem.owner_id = assign_to
        problem.problem_status = status
        problem.save()

        return JsonResponse({
            'status': 'success',
            'message': 'User assigned successfully',
            'assigned_user': {
                'id': assign_to.id,
                'username': assign_to.username
            }
        })

    except Problem.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Problem not found'}, status=404)
    except CustomUser.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required
def problem_feed(request):
    user = request.user
    obj = CustomUser.objects.get(pk=user.pk)
    is_done = request.GET.get('done') == 'true'
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status')
    date_start = request.GET.get('start')
    date_end = request.GET.get('end')
    page = int(request.GET.get('page', 1))

    # Determine project_id for non-user_type requester
    pk = 1
    if obj.setting_user.first():
        pk = obj.setting_user.first().default.pk

    # Base queryset
    project_setting = Project_setting.objects.get(user=obj)
    projects = project_setting.project.all()
    if user.user_type == UserType.objects.get(type_name='Requester'):
        problems_qs = Problem.objects.filter(create_by=user)
    else:
        problems_qs = Problem.objects.filter(project__in=projects)

    # Apply filters
    if not is_done:
        status_done = Status.objects.get(status_en="Done")
        problems_qs = problems_qs.exclude(problem_status=status_done)

    if query:
        problems_qs = problems_qs.filter(
            Q(title__icontains=query) |
            Q(desc__icontains=query) |
            Q(problem_no__icontains=query)
        )

    if status_filter:
        problems_qs = problems_qs.filter(problem_status=status_filter)

    if date_start:
        problems_qs = problems_qs.filter(create_at__date__gte=parse_date(date_start))
    if date_end:
        problems_qs = problems_qs.filter(create_at__date__lte=parse_date(date_end))

    problems_qs = problems_qs.order_by('-update_at')

    # Pagination
    paginator = Paginator(problems_qs, 10)
    page_obj = paginator.get_page(page)
    has_next = page_obj.has_next()

    # Prefetch related data
    problem_ids = [p.pk for p in page_obj]
    dept_ids = set()
    plant_ids = set()

    for p in page_obj:
        if str(p.dept).isdigit():
            dept_ids.add(int(p.dept))
        if str(p.plant).isdigit():
            plant_ids.add(int(p.plant))

    units = Unit.objects.in_bulk(dept_ids) if dept_ids else {}
    plants = Plant.objects.in_bulk(plant_ids) if plant_ids else {}
    attachments = Problem_attachment.objects.filter(problem_id__in=problem_ids)
    replies = Problem_reply.objects.filter(problem_no_id__in=problem_ids)

    attachment_map = defaultdict(list)
    for att in attachments:
        attachment_map[att.problem_id].append(att)

    reply_map = defaultdict(list)
    for r in replies:
        reply_map[r.problem_no_id].append(r)

    # Enrich problem objects
    for problem in page_obj:
        if str(problem.dept).isdigit():
            unit = units.get(int(problem.dept))
            if unit:
                problem.dept = unit.unitName

        if str(problem.plant).isdigit():
            plant = plants.get(int(problem.plant))
            if plant:
                problem.plant = plant.plant_code

        problem.attachments = attachment_map.get(problem.pk, [])
        problem.replies = reply_map.get(problem.pk, [])

    # Load all problem types for filter dropdown
    if user.user_type_id == UserType.objects.get(type_name='Requester'):
        all_problem_status = Problem.objects.filter(
            create_by=user
        ).select_related('problem_status').values_list(
            'problem_status__id', 'problem_status__status_en'
        ).distinct()
    else:
        all_problem_status = Problem.objects.filter(
            project_id=pk
        ).select_related('problem_status').values_list(
            'problem_status__id', 'problem_status__status_en'
        ).distinct()

    # Handle AJAX (lazy loading)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if page_obj.object_list:
            html = render_to_string('problems/problem_feed_list.html', {
                'problems': page_obj,
                'request': request
            }, request=request)
            return JsonResponse({'html': html, 'has_next': has_next})
        else:
            return JsonResponse({'html': '', 'has_next': False})

    # Initial page render
    return render(request, 'problems/problem_feed.html', {
        'problems': page_obj,
        'all_problem_status': all_problem_status,
        'query': query,
        'status_filter': status_filter,
        'date_start': date_start,
        'date_end': date_end,
        'has_next': page_obj.has_next(),
        'pk': pk,
    })


@login_required
def problem_feed_detail(request, pk):
    problem = Problem.objects.get(pk=pk)
    if str(problem.dept).isdigit():
        try:
            unit = Unit.objects.get(pk=problem.dept)
            problem.dept = unit.unitName
        except Unit.DoesNotExist:
            pass

    if str(problem.plant).isdigit():
        try:
            plant = Plant.objects.get(pk=problem.plant)
            problem.plant = plant.plant_code
        except Unit.DoesNotExist:
            pass

    status_html = get_status_dropdown(o_id=problem.id, o_status=problem.problem_status)
    files = Problem_attachment.objects.filter(problem=problem).all()
    problem_reply_form = ProblemReplyForm()
    problem_replys = Problem_reply.objects.filter(problem_no=problem).all()
    table_cnt = range(3-files.count())
    return render(request, 'problems/problem_feed_detail.html', locals())

@login_required
def problem_feed_create(request):
    p = request.GET.get('p')  #單號id
    user = CustomUser.objects.get(pk=request.user.pk)
    project = Project.objects.get(pk=p)
    if request.method == 'POST':
        form = ProblemForm(request.POST, project=project, user=user)
        if form.is_valid():
            with transaction.atomic():
                form_type = get_form_type('PROBLEM')
                tmp_form = form.save(commit=False)
                tmp_form.problem_no = get_serial_num(p, form_type)  # 問題單編碼
                tmp_form.project = project

                # # Safely handle owner assignment
                # owner_id = request.POST.get('owner')
                # if owner_id:  # Only try to get user if owner_id exists and is not empty
                #     try:
                #         tmp_form.owner = CustomUser.objects.get(pk=owner_id)
                #     except (CustomUser.DoesNotExist, ValueError):
                #         # Handle invalid user ID (log error if needed)
                #         tmp_form.owner = None
                # else:
                #     tmp_form.owner = None
                #
                # # Safely handle problem status
                # problem_status_id = request.POST.get('problem_status')
                # if problem_status_id:  # Only try to get user if owner_id exists and is not empty
                #     try:
                #         tmp_form.problem_status_id = problem_status_id
                #     except (ProblemType.DoesNotExist, ValueError):
                #         # Handle invalid user ID (log error if needed)
                #         tmp_form.problem_status = Status.objects.get(status_en="Wait For Assign")
                # else:
                #     tmp_form.problem_status_id = Status.objects.get(status_en="Wait For Assign")

                if request.user.user_type.type_name == "Normal":
                    tmp_form.owner = request.user
                    tmp_form.problem_status = Status.objects.get(status_en="On-Going")
                else:
                    tmp_form.problem_status = Status.objects.get(status_en="Wait For Assign")

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

                # Send WeCom message
                issue_owner_line = f"**Issue Owner**: {tmp_form.owner.username}  \n" if tmp_form.owner_id else ""
                msg = f"""### ⚠️🛠️ [NEW PROBLEM]
                **Problem number**: {tmp_form.problem_no}
                **Problem**: {tmp_form.title}
                **Requester**: {tmp_form.requester}
                **Plant**: {tmp_form.plant.plant_name}
                **Department**: {tmp_form.dept.unitName}
                **Status**: *{tmp_form.problem_status.status_en}*
                {issue_owner_line}\n👉 [Check The Problem Here]({request.build_absolute_uri(tmp_form.get_absolute_url())})
                """
                send_wecom_message(msg)
            if request.user.user_type.type_name == "Requester":
                return redirect('problem_feed_detail', tmp_form.pk)
            return redirect(tmp_form.get_absolute_url())
    else:
        form = ProblemForm(project=project, user=user)

    return render(request, 'problems/problem_feed_edit.html', locals())


@login_required
def problem_feed_edit(request, pk):
    p = request.GET.get('p')  # 單號id
    user = CustomUser.objects.get(pk=request.user.pk)
    project = Project.objects.get(pk=p)

    group_ids = Member.objects.filter(member_id=request.user.pk).values_list('group_id', flat=True)

    group_users = CustomUser.objects.filter(
        pk__in=Member.objects.filter(group_id__in=group_ids).values_list('member_id', flat=True)
    ).distinct()

    if pk:
        problem = Problem.objects.get(pk=pk)
        if not str(problem.plant).isdigit():
            try:
                plant = Plant.objects.get(plant_code=problem.plant)
            except Unit.DoesNotExist:
                pass

    if request.method == 'POST':
        form = ProblemForm(request.POST, instance=problem, project=project, user=user, members=group_users)
        if form.is_valid():
            try:
                with transaction.atomic():
                    tmp_form = form.save(commit=False)
                    selected_owner = form.cleaned_data.get('owner')
                    if selected_owner:
                        tmp_form.owner = selected_owner
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
        form = ProblemForm(instance=problem, project=project, user=user, members=group_users)
    return render(request, 'problems/problem_feed_edit.html', locals())


@login_required
def check_for_user(request):
    problem_id = request.GET.get('problem_id')

    try:
        problem = Problem.objects.get(pk=problem_id)
        check_for_user_status = Status.objects.get(status_en='Check For User')

        problem.problem_status = check_for_user_status
        problem.save()

        # Send WeCom message
        msg = f"""### 🕵️‍♂️ **[CHECK FOR USER CONFIRMATION]**
        **Problem Number**: {problem.problem_no}  
        **Title**: {problem.title}  
        **Requester**: {problem.requester}  
        **Plant**: {problem.plant.plant_name}  
        **Department**: {problem.dept.unitName}
        **Issue Owner**: {problem.owner.username}
        **Status**: *Check For User*  
        👉 [Check The Problem Here]({request.build_absolute_uri(problem.get_absolute_url())})
        """
        send_wecom_message(msg)

        return JsonResponse({'success': True})

    except Problem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Problem not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
def send_notification(request):
    problem_id = request.GET.get('problem_id')

    try:
        problem = Problem.objects.get(pk=problem_id)
        if str(problem.dept).isdigit():
            try:
                unit = Unit.objects.get(pk=problem.dept)
                problem.dept = unit.unitName
            except Unit.DoesNotExist:
                pass

        if str(problem.plant).isdigit():
            try:
                plant = Plant.objects.get(pk=problem.plant)
                problem.plant = plant.plant_code
            except Unit.DoesNotExist:
                pass

        issue_owner_line = f"**Issue Owner**: {problem.owner.username}  \n" if problem.owner_id else ""

        # Send WeCom message
        msg = f"""### 📣 **[PROBLEM REMINDER]**
        **Problem Number**: {problem.problem_no}  
        **Title**: {problem.title}  
        **Requester**: {problem.requester}  
        **Plant**: {problem.plant}  
        **Department**: {problem.dept}  
        **Status**: *{problem.problem_status.status_en}*
        {issue_owner_line}\n⚠ *This is a reminder from the manager. Please check and update the issue.*\n👉 [Check The Problem Here]({request.build_absolute_uri(problem.get_absolute_url())})
        """
        send_wecom_message(msg)

        return redirect(problem.get_absolute_url())

    except Problem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Problem not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
