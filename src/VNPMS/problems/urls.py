from django.urls import re_path as url

from problems.views import *

urlpatterns = [
    url(r'^edit/(?P<pk>\d+)/$', problem_edit, name="problem_edit"),
    url(r'^add/$', problem_create, name="problem_create"),
    url(r'^list/$', problem_list, name="problem_list"),
    url(r'^page/(?P<pk>\d+)/$', problem_page, name="problem_page"),
    url(r'^detail/(?P<pk>\d+)/$', problem_detail, name="problem_detail"),
    url(r'^delete/(?P<pk>\d+)/$', problem_delete, name="problem_delete"),
    url(r'^reply_delete/(?P<pk>\d+)/$', reply_delete, name="problem_reply_delete"),
    url(r'^reply/(?P<pk>\d+)/$', problem_reply_create, name="problem_reply_create"),
    url(r'^pfd/(?P<pk>\d+)/$', problem_file_delete, name="problem_file_delete"),
    url(r'^history', problem_history, name="problem_history"),
    url(r'^chart$', problem_chart, name="problem_chart"),
    url(r'^chart_api$', problem_chart_api, name="problem_chart_api"),
]
