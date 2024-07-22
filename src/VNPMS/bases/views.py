from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from bases.models import Status
from requests.models import Request
from requests.utils import update_process_rate


@login_required
def index(request):
    return render(request, 'bases/index.html', locals())
    #return redirect(reverse('assets_main'))


def change_status(request):
    request_no = request.POST.get('request_no')
    new_status = request.POST.get('new_status')
    o_new_status = Status.objects.get(pk=new_status)
    the_request = Request.objects.filter(request_no=request_no).first()
    the_request.status = o_new_status
    the_request.process_rate = update_process_rate(the_request.request_no, o_new_status)
    the_request.save()

    result = {'message': 'good'}

    return JsonResponse(result, safe=False)


def get_user_setting_pagenum(request):
    page_num = 5
    # 取得使用者專案設定
    if request.user.setting_user:
        project_setting = request.user.setting_user.first()
        page_num = project_setting.page_number
    return page_num

