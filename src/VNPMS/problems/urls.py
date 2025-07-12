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
    url(r'^chart_grid_api$', problem_chart_grid_api, name="problem_chart_grid_api"),
    url(r'^assign/(?P<problem_id>\d+)/$', assign_problem, name="assign_problem"),
    url(r'change_status', change_status, name="problem_change_status"),
    url(r'load-depts', load_depts, name='load_depts'),
    url(r'^receive', problem_receive, name="problem_receive"),
    url(r'^feed$', problem_feed, name="problem_feed"),
    url(r'^feed_detail/(?P<pk>\d+)/$', problem_feed_detail, name="problem_feed_detail"),
    url(r'^feed_edit/(?P<pk>\d+)/$', problem_feed_edit, name="problem_feed_edit"),
    url(r'^feed_add/$', problem_feed_create, name="problem_feed_create"),
    url(r'^check_for_user/$', check_for_user, name="check_for_user"),
    url(r'^send_notification/$', send_notification, name="send_problem_notification"),
]
