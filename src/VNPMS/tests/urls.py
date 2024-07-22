from django.urls import re_path as url
from tests.views import rtest_create, rtest_form, rtest_edit, rtest_result, rtest_delete

urlpatterns = [
    # url(r'^edit/(?P<pk>\d+)/$', rtest_edit, name="request_edit"),
    url(r'^add/$', rtest_create, name="rtest_create"),
    url(r'^edit/$', rtest_edit, name="rtest_edit"),
    url(r'^delete/$', rtest_delete, name="rtest_delete"),
    url(r'^form/(?P<pk>\d+)/$', rtest_form, name="rtest_form"),
    url(r'^result/(?P<r>\d+)/$', rtest_result, name="rtest_result"),
]
