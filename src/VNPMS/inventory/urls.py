from django.urls import re_path as url
from inventory.views import main, apply, TypeAPI, ItemAPI, detail, agree, apply_list, approve, reject, import_excel, \
    statistic, change_status, delete, mail_reject, mail_agree, recieved, pr_apply, search, item_list, item_detail, \
    item_update, item_create, setting, export_form_xls, CategoryAPI, template_edit

urlpatterns = [
    url(r'^main/', main, name='inv_main'),
    url(r'^apply/', apply, name='inv_apply'),
    url(r'^pr_apply/', pr_apply, name='inv_pr_apply'),
    url(r'^typeapi/(?P<category_id>\d+)', TypeAPI, name='catogory_typeapi'),
    url(r'^itemapi/', ItemAPI, name='catogory_itemapi'),
    url(r'^detail/(?P<pk>\w+)/$', detail, name='inv_detail'),
    url(r'^delete/(?P<pk>\w+)/$', delete, name='inv_delete'),
    url(r'^agree/(?P<key>\w+)/$', agree, name='inv_agree'),
    url(r'^reject/(?P<key>\w+)/$', reject, name='inv_reject'),
    url(r'^list/', apply_list, name='inv_list'),
    url(r'^approve/', approve, name='inv_approve'),
    url(r'^import/', import_excel, name='inv_import'),
    url(r'^statistic/', statistic, name='inv_statistic'),
    url(r'^change_status/', change_status, name='inv_change_status'),
    url(r'^mail_reject/(?P<key>\w+)/$', mail_reject, name='inv_mail_reject'),
    url(r'^mail_agree/(?P<key>\w+)/$', mail_agree, name='inv_mail_agree'),
    url(r'^recieved/(?P<pk>\w+)/$', recieved, name='inv_recieved'),
    url(r'^search/', search, name='inv_search'),
    url(r'^item_list/', item_list, name='item_list'),
    url(r'^item_detail/(?P<pk>\w+)/$', item_detail, name='item_detail'),
    url(r'^item_update/(?P<pk>\d+)/$', item_update, name='item_update'),
    url(r'^item_create/', item_create, name='item_create'),
    url(r'^setting/', setting, name='inv_setting'),
    url(r'^export_form_xls/', export_form_xls, name='export_form_xls'),
    url(r'^categoryapi/(?P<family_id>\d+)', CategoryAPI, name='item_categoryapi'),
    url(r'^typeapi/(?P<category_id>\d+)', TypeAPI, name='item_typeapi'),
    url(r'^template_edit/', template_edit, name='template_edit'),
]
