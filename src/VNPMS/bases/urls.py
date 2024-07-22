from django.urls import re_path as url
from bases.views import change_status, index

urlpatterns = [
    url(r'^change_status$', change_status, name='change_status'),
    url(r'^', index, name='index'),
]
