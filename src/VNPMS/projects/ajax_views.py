import time

from django.http import JsonResponse

from bases.models import FormType
from bugs.models import Bug
from problems.models import Problem, Problem_reply
from requests.models import Request
from requests.utils import cal_sub_requests, cal_problems


# def getChildvalue(request_pk):
#     result = '0'
#     count = Request.objects.filter(belong_to=request_pk).count()
#     if count > 0:
#         result = '1'
#     return result


# def getChild(request, pk):
#     requests = Request.objects.filter(belong_to=pk)
#     requests = cal_sub_requests(requests)
#     requests = cal_problems(requests)
#     request_json = request2json(request, requests)
#
#     return JsonResponse(request_json, safe=False)


# def getBug(request, pk):
#     bugs = Bug.objects.filter(project=pk)
#     bug_json = bug2json(bugs)
#
#     return JsonResponse(bug_json, safe=False)


# def getAllProblem(request, pk):
#     problems = Problem.objects.filter(project=pk)
#     problem_json = problem2json(problems)
#
#     return JsonResponse(problem_json, safe=False)

# def getProblem2(request):
#     no = ''
#     form_type = FormType.objects.filter(tid=tid).first()
#     # 依表單類型找對應單號
#     if form_type.type == 'REQUEST':
#         no = Request.objects.get(pk=pk).request_no
#     if form_type.type == 'BUG':
#         no = Bug.objects.get(pk=pk).bug_no
#
#     problems = Problem.objects.filter(belong_to_type=form_type, belong_to=no)
#     problem_json = problem2json(problems)
#
#     return JsonResponse(problem_json, safe=False)


# def getProblem(request, tid, pk):
#     no = ''
#     form_type = FormType.objects.filter(tid=tid).first()
#     # 依表單類型找對應單號
#     if form_type.type == 'REQUEST':
#         no = Request.objects.get(pk=pk).request_no
#     if form_type.type == 'BUG':
#         no = Bug.objects.get(pk=pk).bug_no
#
#     problems = Problem.objects.filter(belong_to_type=form_type, belong_to=no).all()
#     problem_json = problem2json(problems)
#
#     return JsonResponse(problem_json, safe=False)


#
# def getChildByProj(request, pk):
#     o_requests = Request.objects.filter(project=pk, belong_to__isnull=True)
#     o_requests = cal_sub_requests(o_requests)
#     o_requests = cal_problems(o_requests)
#     request_json = request2json(request, o_requests)
#
#     return JsonResponse(request_json, safe=False)

#
# def request2json(request, o_requests):
#     request_json = []
#     for o_request in o_requests:
#         rr = {}
#         rr['pk'] = o_request.pk
#         if request.user.is_authenticated():
#             rr['num'] = "<a href='/requests/detail/"+str(o_request.pk)+"'>" + str(o_request.request_no) + "</a>"
#         else:
#             rr['num'] = "<a href='/requests/" + str(o_request.request_no) + "'>" + str(o_request.request_no) + "</a>"
#         rr['title'] = str(o_request.title)
#         rr['level'] = str(o_request.level)
#         rr['status'] = str(o_request.status)
#         rr['owner'] = str(o_request.owner)
#         rr['starttime'] = str(o_request.start_date)
#         rr['finishtime'] = str(o_request.due_date)
#         rr['rate'] = o_request.process_rate
#         rr['subrequire'] = o_request.sub_num
#         rr['question'] = o_request.problem_num
#         rr['nested'] = getChildvalue(rr['pk'])
#
#         request_json.append(rr)
#     return request_json


def problem2json(problems):
    problem_json = []
    for problem in problems:
        rr = {}
        rr['pk'] = problem.pk
        rr['problem_no'] = "<a href='/problems/detail/"+str(problem.pk)+"'>" + str(problem.problem_no) + "</a>"
        rr['title'] = str(problem.title)
        rr['reply_num'] = Problem_reply.objects.filter(problem_no=problem.pk).count()
        rr['create_by'] = str(problem.create_by)
        rr['create_at'] = problem.create_at.strftime("%Y-%m-%d %H:%M:%S")
        rr['update_by'] = str(problem.update_by)
        rr['update_at'] = problem.update_at.strftime("%Y-%m-%d %H:%M:%S")

        problem_json.append(rr)
    return problem_json


def bug2json(bugs):
    problem_json = []
    for bug in bugs:
        rr = {}
        rr['pk'] = bug.pk
        rr['bug_no'] = "<a href='/bugs/detail/"+str(bug.pk)+"'>" + str(bug.bug_no) + "</a>"
        rr['title'] = str(bug.title)
        rr['level'] = str(bug.level)
        rr['owner'] = str(bug.owner)
        rr['create_by'] = str(bug.create_by)
        rr['create_at'] = bug.create_at.strftime("%Y-%m-%d %H:%M:%S")

        problem_json.append(rr)
    return problem_json