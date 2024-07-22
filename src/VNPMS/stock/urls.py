from django.urls import re_path as url
from stock.views import search, location_setting, storage_edit, location_list, location_add, location_edit, \
    location_save, bin_add, bin_edit, bin_save, bin_list, stock_in, stock_out, item_search_popup, TypeAPI, ItemAPI, \
    stockin_detail, get_item_info, bin_search_popup, LocationAPI, get_bin_info, stockout_detail, StockItemAPI, \
    item_stock_search_popup, recent_history, stock_history, stock_search, stock_search_action, stock_search_excel, \
    StorageBinAPI, LocationBinAPI, stockin_search, stockout_search

urlpatterns = [
    url(r'^search/', search, name='stock_search'),
    url(r'^item_search_popup/', item_search_popup, name='item_search_popup'),
    url(r'^item_stock_search_popup/', item_stock_search_popup, name='item_stock_search_popup'),
    url(r'^bin_search_popup/', bin_search_popup, name='bin_search_popup'),
    url(r'^location_setting/', location_setting, name='location_setting'),
    url(r'^location/', location_list, name='location_list'),
    url(r'^location_add/', location_add, name='location_add'),
    url(r'^location_edit/', location_edit, name='location_edit'),
    url(r'^location_save/', location_save, name='location_save'),
    url(r'^location_api/(?P<storage_code>\w+)', LocationAPI, name='stock_location_api'),
    url(r'^storage_edit/', storage_edit, name='storage_edit'),
    url(r'^storage_bin_api/', StorageBinAPI, name='storage_bin_api'),
    url(r'^location_bin_api/(?P<location_code>\w+)', LocationBinAPI, name='location_bin_api'),
    url(r'^bin/(?P<storage_code>\w+)/(?P<location_code>[\w-]+)', bin_list, name='bin_list'),
    url(r'^bin_add/', bin_add, name='bin_add'),
    url(r'^bin_edit/', bin_edit, name='bin_edit'),
    url(r'^bin_save/', bin_save, name='bin_save'),
    url(r'^stock_in/', stock_in, name='stock_in'),
    url(r'^stockin_detail/(?P<pk>\w+)/$', stockin_detail, name='stockin_detail'),
    url(r'^stock_out/', stock_out, name='stock_out'),
    url(r'^stockout_detail/(?P<pk>\w+)/$', stockout_detail, name='stockout_detail'),
    url(r'^typeapi/(?P<category_id>\d+)', TypeAPI, name='stock_typeapi'),
    url(r'^itemapi/', ItemAPI, name='stock_catogory_itemapi'),
    url(r'^stockitemapi/', StockItemAPI, name='stock_catogory_stockitemapi'),
    url(r'^getitemapi/', get_item_info, name='stock_get_item_info'),
    url(r'^getbinapi/', get_bin_info, name='stock_get_bin_info'),
    url(r'^recent_history/', recent_history, name='recent_history'),
    url(r'^stock_history/', stock_history, name='stock_history'),
    url(r'^stock_search/', stock_search, name='stock_search'),
    url(r'^stock_search_excel/', stock_search_excel, name='stock_search_excel'),
    url(r'^stock_search_action/', stock_search_action, name='stock_search_action'),
    url(r'^stockin_search/', stockin_search, name='stockin_search'),
    url(r'^stockout_search/', stockout_search, name='stockout_search'),
]