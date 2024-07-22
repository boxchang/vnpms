from django.urls import re_path as url
from assets.views import TypeAPI, BrandAPI, asset_doc_delete, asset_pic_delete, export_assets_xls, index, label, \
    main, delete, print_label, update, create, search, import_excel, detail, import_assets_preview, label_preview, \
    chart, chart_api, asset_history, category_reset

urlpatterns = [
    url(r'^print_label/(?P<pk>\d+)/$', print_label, name='print_label'),
    url(r'^brandapi/(?P<category_id>\d+)', BrandAPI, name='assets_brandapi'),
    url(r'^typeapi/(?P<category_id>\d+)', TypeAPI, name='assets_typeapi'),
    url(r'^import/', import_excel, name='assets_import'),
    url(r'^export/xls/$', export_assets_xls, name='export_assets_xls'),
    url(r'^main/', main, name='assets_main'),
    url(r'^search/', search, name='assets_search'),
    url(r'^create/', create, name='assets_create'),
    url(r'^delete/(?P<pk>\d+)/$', delete, name='assets_delete'),
    url(r'^update/(?P<pk>\d+)/$', update, name='assets_update'),
    url(r'^detail/(?P<pk>\d+)/$', detail, name='assets_detail'),
    url(r'^import_assets_preview/', import_assets_preview, name='import_assets_preview'),
    url(r'^label_preview/', label_preview, name='label_preview'),
    url(r'^label/', label, name='assets_label'),
    url(r'^chart/', chart, name='assets_chart'),
    url(r'^chart_api/', chart_api, name='chart_api'),
    url(r'^dpic/(?P<pk>\d+)', asset_pic_delete, name="asset_pic_delete"),
    url(r'^ddoc/(?P<pk>\d+)', asset_doc_delete, name="asset_doc_delete"),
    url(r'^history/(?P<pk>\d+)', asset_history, name="asset_history"),
    url(r'^category_reset/', category_reset, name="category_reset"),
    url(r'^', index, name='assets_index'),
]
