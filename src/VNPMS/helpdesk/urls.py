from django.urls import re_path as url
from helpdesk.views import helpdesk_edit, helpdesk_create, helpdesk_detail, helpdesk_delete, helpdesk_file_delete, helpdesk_file_delete, search, helpdesk_guest, index

urlpatterns = [
    url(r'^edit/(?P<pk>\d+)/$', helpdesk_edit, name="helpdesk_edit"),
    url(r'^add/$', helpdesk_create, name="helpdesk_create"),
    url(r'^detail/(?P<pk>\d+)/$', helpdesk_detail, name="helpdesk_detail"),
    url(r'^delete/(?P<pk>\d+)/$', helpdesk_delete, name="helpdesk_delete"),
    url(r'^rfd/(?P<pk>\d+)', helpdesk_file_delete, name="helpdesk_file_delete"),
    url(r'^search/$', search, name="search"),
    url(r'^(?P<help_no>\w+)$', helpdesk_guest, name="helpdesk_guest"),
    url(r'^', index, name='help_index'),
]
