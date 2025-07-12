from django.urls import re_path as url

from users.views import *

urlpatterns = [
    url(r'^register/$', register, name='register'),
    url(r'^signup/$', sign_up, name='signup'),
    url(r'^signup/request$', sign_up_request, name='signup_request'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^create/$', create, name='user_create'),
    url(r'^list/$', user_list, name='user_list'),
    url(r'^detail/$', detail, name='user_detail'),
    url(r'^user_edit/$', user_edit, name='user_edit'),
    url(r'^user_info/$', user_info, name='user_info'),
    url(r'^user_auth_api/$', user_auth_api, name='user_auth_api'),
    url(r'^unit_list/$', unit_list, name='unit_list'),
    url(r'^unit_sync/$', unit_sync, name='unit_sync'),
    url(r'^user_sync/$', user_sync, name='user_sync'),
    url(r'^get_deptuser_api/', get_deptuser_api, name='get_deptuser_api'),
    url(r'^approve/$', user_approving, name='user_approving'),
    url(r'^decline/$', user_declining, name='user_declining'),
    url(r'^group/$', group_management, name='group_management'),
    url(r'^group/edit$', group_edit, name='group_edit'),
    url(r'^group/invitation$', send_invitation, name='group_send_invitation'),
    url(r'^group/respond', respond_invitation, name='group_respond_invitation'),
    url(r'^group/remove_member', remove_member, name='group_remove_member'),
    url(r'^group/delete/(?P<group_id>\d+)/$', group_delete, name='group_delete')
]
