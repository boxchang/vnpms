from django.urls import re_path as url
from borrow.views import apply, get_asset_api, find_asset_api, record, get_borrow_item_api, detail, \
    update, form_delete, item_delete

urlpatterns = [
    url(r'^apply/', apply, name='apply'),
    url(r'^record/', record, name='record'),
    url(r'^detail/(?P<form_no>\d+)/', detail, name='detail'),
    url(r'^update/(?P<pk>\d+)/$', update, name='borrow_update'),
    url(r'^item_delete/(?P<form_no>\d+)/(?P<asset_id>\d+)/', item_delete, name='borrow_item_delete'),
    url(r'^form_delete/(?P<form_no>\d+)/', form_delete, name='form_delete'),
    url(r'^(?P<pk>\d+)/item/', get_borrow_item_api, name='get_borrow_item_api'),
    url(r'^get_asset_api/', get_asset_api, name='get_asset_api'),
    url(r'^find_asset_api/', find_asset_api, name='find_asset_api'),
]
