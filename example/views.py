# -*- coding: utf-8 -*-

from django.views.generic import TemplateView


class UsersDash(TemplateView):
    template_name = "chartflo/dashboards/users.html"