# -*- coding: utf-8 -*-

from __future__ import print_function
from chartflo.models import Chart
from .charts import serialize_last_logins, serialize_user_groups


def run():
    """
    Run the job
    """
    # Last logins chart
    slug = "last_logins"
    name = "Last logins"
    dataset = serialize_last_logins(slug)
    chart, _ = Chart.objects.get_or_create(slug=slug)
    chart.save_from_dataset(chart, slug, name, dataset)
    print("[ ok ] Chart", slug, "saved")
    # User groups chart
    slug = "user_groups"
    name = "User groups"
    dataset = serialize_user_groups(slug)
    chart, _ = Chart.objects.get_or_create(slug=slug)
    chart.save_from_dataset(chart, slug, name, dataset)
    print("[ ok ] Chart", slug, "saved")
