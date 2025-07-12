from django.urls import re_path as url

from projects.ajax_views import *
from requests.views import *

urlpatterns = [
    url(r'^page/(?P<pk>\d+)/$', request_page, name="request_page"),
    url(r'^edit/(?P<pk>\d+)/$', request_edit, name="request_edit"),
    url(r'^add/$', request_create, name="request_create"),
    url(r'^list/$', request_list, name="request_list"),
    url(r'^detail/(?P<pk>\d+)/$', request_detail, name="request_detail"),
    url(r'^delete/(?P<pk>\d+)/$', request_delete, name="request_delete"),
    url(r'^$', get_request, name="get_request"),
    url(r'^index/(?P<pk>\d+)/$', request_index, name="request_index"),
    url(r'^receive', request_receive, name="request_receive"),
    url(r'change_status', change_status, name="change_status"),
    url(r'^rfd/(?P<pk>\d+)', request_file_delete, name="request_file_delete"),
    url(r'^history', request_history, name="request_history"),
    url(r'^(?P<no>\w+)$', request_guest, name="request_guest"),
    url(r'^reply/(?P<pk>\d+)/$', request_reply, name="request_reply"),
    url(r'^reply_delete/(?P<pk>\d+)/$', reply_delete, name="request_reply_delete"),
    url(r'^reply_edit/(?P<pk>\d+)/$', reply_edit, name="reply_edit"),
    url(r'^send_notification/$', send_notification, name="send_request_notification"),
]
