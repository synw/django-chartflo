# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import DashboardView, getDashboardPageView, getDashboardIndexView


urlpatterns = [
    url(r'^page/(?P<dashboard_name>[-_\w\d]+)/(?P<page_name>[-_\w]+)/$',
        getDashboardPageView, name="dashboard-page"),
    url(r'^page/(?P<dashboard_name>[-_\w\d]+)/$',
        getDashboardIndexView, name="dashboard-index"),
    url(r'^(?P<dashboard_name>[-_\w]+)/$',
        DashboardView.as_view(), name="dashboard")
]