# -*- coding: utf-8 -*-

from __future__ import print_function
from django.contrib.auth.models import User
from chartflo.factory import ChartController


def serialize_last_logins(slug):
    """
    Get the charts data and serialize it
    """
    print("Serializing", slug, "chart ...")
    chart_type = "square"
    x = ("last_login", "last_login:T")
    y = ("username", "count(username):Q")
    width = 800
    height = 150
    users = User.objects.all().order_by("last_login")
    chart = ChartController()
    dataset = chart.serialize_timeseries(
        users, x, y, time_unit="yearmonth", chart_type=chart_type,
        width=width, height=height, color="username", size="username"
    )
    return dataset


def serialize_user_groups(slug):
    print("Serializing", slug, "chart ...")
    chart_type = "bar"
    x = ("group", "group")
    y = ("number", "number:Q")
    width = 550
    height = 250
    users = User.objects.all()
    staff = users.filter(is_staff=True)
    superusers = users.filter(is_superuser=True)
    others = users.filter(is_superuser=False, is_staff=False)
    dataset = {"users": others.count(), "staff": staff.count(),
               "superuser": superusers.count()}
    chart = ChartController()
    datapack = chart.serialize_count(
        dataset, x, y, chart_type=chart_type,
        width=width, height=height, color="group"
    )
    return datapack
