# -*- coding: utf-8 -*-

from __future__ import print_function
from django.contrib.auth.models import User
from chartflo.factory import ChartController, NumberController


GENERATOR = "chart_users"


def run():
    """
    Run the job
    """
    global GENERATOR
    users = User.objects.all()
    num = NumberController()
    # Num users
    val = users.count()
    num.generate("users", "Users", val, modelnames="User", generator=GENERATOR)
    # Num emails
    emails = 0
    for user in users:
        if user.email != "":
            emails += 1
    num.generate("emails", "Emails", emails,
                 modelnames="User", generator=GENERATOR)
    # Num names
    names = 0
    for user in users:
        if user.first_name != "" and user.last_name != "":
            names += 1
    num.generate("names", "Names", names,
                 modelnames="User", generator=GENERATOR)
    # Num users
    val = users.filter(is_staff=True).count()
    num.generate("staff", "Staff", val, generator=GENERATOR)
    # Num users
    val = users.filter(is_superuser=True).count()
    num.generate("superusers", "Superusers", val,
                 modelnames="User", generator=GENERATOR)
    # Last logins chart
    chart = ChartController()
    x = ("last_login", "last_login:T")
    y = ("username", "count(username):Q")
    q = users.order_by("last_login")
    chart.generate(
        "last_logins", "Last logins", "line", q, x, y, 870, 180,
        time_unit="yearmonth", verbose=True, modelnames="User", generator=GENERATOR
    )
    # date joined chart
    q = users.order_by("date_joined")
    x = ("date_joined", "date_joined:T")
    y = ("username", "count(username):Q")
    chart.generate(
        "date_joined", "Date joined", "line", q, x, y, 870, 180,
        time_unit="yearmonth", verbose=True, modelnames="User", generator=GENERATOR
    )
    # User groups chart
    x = ("group", "group")
    y = ("number", "number:Q")
    staff = users.filter(is_staff=True)
    superusers = users.filter(is_superuser=True)
    others = users.filter(is_superuser=False, is_staff=False)
    dataset = {"users": others.count(), "staff": staff.count(),
               "superuser": superusers.count()}
    chart.generate(
        "user_groups", "User groups", "bar", dataset, x, y, 350, 250,
        color="group", verbose=True, modelnames="User,Group", generator=GENERATOR
    )
