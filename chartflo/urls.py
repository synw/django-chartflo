# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import DashboardView


urlpatterns = [
    url(r'^(?P<slug>[-_\w]+)/$', DashboardView.as_view(), name="dashboard")
]
