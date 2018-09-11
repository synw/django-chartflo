# -*- coding: utf-8 -*-
import os
from django import template

register = template.Library()


@register.simple_tag
def get_altair_scripts(dashboard_slug):
    path = "dashboards/" + dashboard_slug + "/altair_scripts"
    scripts = os.listdir("templates/" + path)
    includes = []
    for script in scripts:
        includes.append(path + "/" + script)
    return includes
