# -*- coding: utf-8 -*-

from __future__ import print_function
from django.contrib.auth.models import User
from chartflo.factory import ChartController
from .generators.numbers import gen_numbers


def run():
    """
    Run the job
    """
    # Num users
    gen_numbers()
    # Last logins chart
    chart = ChartController()
    x = ("last_login", "last_login:T")
    y = ("username", "count(username):Q")
    users = User.objects.all()
    q = users.order_by("last_login")
    chart.generate(
        "last_logins", "Last logins", "line", q, x, y, 870, 180, "yearmonth", verbose=True)
    # date joined chart
    q = users.order_by("date_joined")
    x = ("date_joined", "date_joined:T")
    y = ("username", "count(username):Q")
    chart.generate(
        "date_joined", "Date joined", "line", q, x, y, 870, 180, "yearmonth", verbose=True)
    # User groups chart
    x = ("group", "group")
    y = ("number", "number:Q")
    staff = users.filter(is_staff=True)
    superusers = users.filter(is_superuser=True)
    others = users.filter(is_superuser=False, is_staff=False)
    dataset = {"users": others.count(), "staff": staff.count(),
               "superuser": superusers.count()}
    chart.generate(
        "user_groups", "User groups", "bar", dataset, x, y, 350, 250, color="group", verbose=True)
