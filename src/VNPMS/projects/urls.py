from django.urls import re_path as url

from projects.views import *

urlpatterns = [
    url(r'^$', index),
    url(r'^edit/(?P<pk>\d+)/$', project_edit, name="project_edit"),
    url(r'^delete/(?P<pk>\d+)/$', project_delete, name="project_delete"),
    url(r'^add/$', project_create, name="project_create"),
    url(r'^list/$', project_list, name="project_list"),
    url(r'^manage/(?P<pk>\d+)/$', project_manage, name="project_manage"),
    url(r'^setting/$', project_setting, name="project_setting"),
    url(r'^search/$', search, name="search"),
    url(r'^home', pms_home, name='pms_home'),
]
