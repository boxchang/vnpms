from django.urls import re_path as url

from bugs.views import *

urlpatterns = [
    url(r'^edit/(?P<pk>\d+)/$', bug_edit, name="bug_edit"),
    url(r'^add/$', bug_create, name="bug_create"),
    url(r'^list/$', bug_list, name="bug_list"),
    url(r'^page/(?P<pk>\d+)/$', bug_page, name="bug_page"),
    url(r'^detail/(?P<pk>\d+)/$', bug_detail, name="bug_detail"),
    url(r'^delete/(?P<pk>\d+)/$', bug_delete, name="bug_delete"),
    url(r'^bfd/(?P<pk>\d+)', bug_file_delete, name="bug_file_delete"),
]
