"""VNPMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.urls import re_path as url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter

from borrow.ser_views import BorrowByViewSet
from bugs.ser_views import BugByPViewSet
from problems.ser_views import ProblemByPViewSet, ProblemByRViewSet, ProblemByBViewSet
from bases.views import index
from django.conf.urls.static import static
from django.conf import settings

from requests.ser_views import SubRequestViewSet, RequestByPViewSet

router = DefaultRouter()
router.register(r'requests/(?P<request_id>\d+)/requests', SubRequestViewSet)
router.register(r'requests/(?P<request_id>\w+)/problems', ProblemByRViewSet)
router.register(r'projects/(?P<project_id>\d+)/(?P<user_id>\d+)/requests', RequestByPViewSet)
router.register(r'projects/(?P<project_id>\d+)/(?P<user_id>\d+)/problems', ProblemByPViewSet)
router.register(r'projects/(?P<project_id>\d+)/(?P<user_id>\d+)/bugs', BugByPViewSet)
router.register(r'bugs/(?P<bug_id>\d+)/problems', ProblemByBViewSet)
router.register(r'borrow', BorrowByViewSet)

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^stock/', include('stock.urls')),
    url(r'^monitor/', include('monitor.urls')),
    url(r'^production/', include('production.urls')),
    url(r'^inventory/', include('inventory.urls')),
    url(r'^borrow/', include('borrow.urls')),
    url(r'^projects/', include('projects.urls')),
    url(r'^requests/', include('requests.urls')),
    url(r'^problems/', include('problems.urls')),
    url(r'^home', include('bases.urls')),
    url(r'^bugs/', include('bugs.urls')),
    url(r'^tests/', include('tests.urls')),
    url(r'^helpdesk/', include('helpdesk.urls')),
    url(r'^assets/', include('assets.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    url(r'^$', index, name='index'),
    url(r'^users/', include('users.urls')),
)
