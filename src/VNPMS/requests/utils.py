from problems.models import *
from requests.models import Request, Request_attachment


#  更新完成度
def update_process_rate(belong_to):
    rate = 0

    requests = Request.objects.filter(belong_to=belong_to)

    for request in requests:
        rate += request.status.process_rate
    rate = rate / requests.count()

    obj = Request.objects.get(pk=belong_to.id)
    obj.process_rate = rate
    obj.save()


#  計算子需求及完成度
def cal_sub_requests(requests):
    for f_request in requests:
        f_num = 0
        sub_requests = Request.objects.filter(belong_to=f_request)
        f_request.sub_num = '-'
        if sub_requests.count() > 0:
            for sub_request in sub_requests:
                if sub_request.process_rate == 100:
                    f_num += 1
            f_request.sub_num = '{sub_request}/{total_request}'.format(sub_request=str(f_num), total_request=str(sub_requests.count()))
            f_request.process_rate = int((f_num / sub_requests.count()) *100)
    return requests


#  計算問題數量
def cal_problems(requests):
    for f_request in requests:
        f_request.problem_num = Problem.objects.filter(belong_to=f_request).count()
    return requests

