from django.urls import re_path as url

from monitor.views import index

urlpatterns = [
    url(r'^', index, name='monitor_index'),
]