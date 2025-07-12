import socket
import datetime
from django.utils.translation import gettext as _
from django.http import Http404
from django.urls import reverse
from bases.models import DataIndex, FormType, Status
from inventory.models import FormStatus
from projects.models import Project
from users.models import CustomUser
import httpx
from httpx import RequestError
from VNPMS.settings.base import WECOM_APP_PROBLEM


def get_all_formtype():
    formtype = {}
    objs = FormType.objects.all()
    for obj in objs:
        formtype.update({obj.form_type: obj.form_id})
    return formtype


def get_form_type(form_type):
    try:
        obj = FormType.objects.filter(type=form_type).first()
    except FormType.DoesNotExist:
        raise Http404

    return obj


def get_datetime_str():
    now = datetime.datetime.now()
    return now.strftime("%Y%m%d%H%M%S")


def get_date_str():
    now = datetime.datetime.now()
    return now.strftime("%Y%m%d")


def save_data_index(project, form_type):
    project = Project.objects.get(pk=project)
    obj = DataIndex.objects.filter(project=project, data_type=form_type.tid, data_date=get_date_str()).last()
    if obj:
        obj.current += 1
        obj.save()
    else:
        DataIndex.objects.create(project=project, data_type=form_type.tid, data_date=get_date_str(), current=1)

def get_data_index(project, form_type):
    obj = DataIndex.objects.filter(project=project, data_type=form_type.tid, data_date=get_date_str()).last()
    if obj:
        index = obj.current + 1
    else:
        index = 1
    return index

def get_serial_num(pk, form_type):
    project = Project.objects.get(pk=pk)
    no_first = project.short_name
    no_middle = get_date_str()
    no_last = form_type.short_name + str(get_data_index(project, form_type)).zfill(3)
    return no_first + no_middle + no_last

def get_form_json(form):
    json = ''
    for field in form.fields:
        json += "{field:'"+ field +"', title: '"+ form[field].label +"'},"
    json += "{'field': 'pk', 'title': '鍵值', 'visible': 'false'}"
    json = "["+json+"]"
    return json


def get_home_url(request):
    obj = CustomUser.objects.get(pk=request.user.pk)
    pk = obj.setting_user.first().default.pk

    if pk:
        return reverse('project_manage', kwargs={'pk': pk})
    else:
        return reverse('login')


def get_status_dropdown(o_id, o_status):
    tmp = ""
    status_html = """<div class="btn-group dropdown">
                      <button class="btn btn-info dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        {title}
                      </button>
                      <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                        {tmp}
                      </div>
                    </div>
                    <input type="hidden" name="o_id" id="o_id" value={o_id} \>
                    <input type="hidden" name="status_id" id="status_id" \>
                    """

    status = Status.objects.all()
    for s in status:
        active = ""
        if s == o_status:
            active = "active"
        tmp += "<a class=\"dropdown-item {active}\" href=\"#\" onclick=\"change_status('{status_value}');\">{status_name}</a>"
        tmp = tmp.format(active=active, status_value=s.id, status_name=s.status_en)

    status_html = status_html.format(title=_("Update Status"), tmp=tmp, o_id=o_id)
    return status_html


def get_invform_status_dropdown(o_form):
    tmp = ""
    status_html = """<div class="btn-group dropdown">
                      <button class="btn btn-info dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        {title}
                      </button>
                      <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                        {tmp}
                      </div>
                    </div>
                    <input type="hidden" name="form_id" id="form_id" value={form_id} \>
                    <input type="hidden" name="status_id" id="status_id" \>
                    """

    status = FormStatus.objects.all()
    for s in status:
        active = ""
        if s == o_form.status:
            active = "active"
        tmp += "<a class=\"dropdown-item {active}\" href=\"#\" onclick=\"change_status('{status_value}');\">{status_name}</a>"
        tmp = tmp.format(active=active, status_value=s.id, status_name=s.status_name)

    status_html = status_html.format(title=_("Update Status"), tmp=tmp, form_id=o_form.form_no)
    return status_html


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def get_batch_no():
    now = datetime.datetime.now()
    batch_no = now.strftime("%y%m%d%H%M%S")
    return batch_no


def send_wecom_message(message: str):
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": message,
        }
    }

    try:
        response = httpx.post(WECOM_APP_PROBLEM, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except RequestError as e:
        return {"error": str(e)}

