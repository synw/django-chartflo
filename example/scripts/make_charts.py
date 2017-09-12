# -*- coding: utf-8 -*-

from __future__ import print_function
from chartflo.models import Chart
from blessings import Terminal
from .generators.charts import serialize_last_logins, serialize_user_groups, serialize_date_joined
from .generators.numbers import gen_numbers


def run():
    """
    Run the job
    """
    color = Terminal()
    ok = color.bold_green("ok")
    # Num users
    gen_numbers()
    # Last logins chart
    slug = "last_logins"
    name = "Last logins"
    dataset = serialize_last_logins(slug)
    chart, _ = Chart.objects.get_or_create(slug=slug)
    chart.generate(chart, slug, name, dataset)
    print("[" + ok + "] Chart", color.bold(slug), "saved")
    # date_joined chart
    slug = "date_joined"
    name = "Date joined"
    dataset = serialize_date_joined(slug)
    chart, _ = Chart.objects.get_or_create(slug=slug)
    chart.generate(chart, slug, name, dataset)
    print("[" + ok + "] Chart", color.bold(slug), "saved")
    # User groups chart
    slug = "user_groups"
    name = "User groups"
    dataset = serialize_user_groups(slug)
    chart, _ = Chart.objects.get_or_create(slug=slug)
    chart.generate(chart, slug, name, dataset)
    print("[" + ok + "] Chart", color.bold(slug), "saved")
