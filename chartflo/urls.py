# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import DashboardView, getDashboardPageView


urlpatterns = [
    url(r'^page/(?P<slug>[-_\w]+)/$',
        getDashboardPageView, name="dashboard-page"),
    url(r'^(?P<slug>[-_\w]+)/$', DashboardView.as_view(), name="dashboard")
]
