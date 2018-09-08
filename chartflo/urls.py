# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import DashboardView, getDashboardView

urlpatterns = [
    url(r'^(?P<dashboard_name>[-_\w]+)/(?P<view_name>[-_\w]+)/$',
        getDashboardView, name="dashboard-view"),
    url(r'^(?P<dashboard_name>[-_\w]+)/$',
        DashboardView.as_view(), name="dashboard"),
]
