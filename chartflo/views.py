# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.http.response import Http404
from .conf import ENGINE


class DashboardView(TemplateView):
    """
    Generic dashboard view
    """

    def dispatch(self, request, *args, **kwargs):
        self.slug = kwargs["slug"]
        if not request.user.is_superuser is True:
            return Http404
        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def get_template_names(self, *args, **kwargs):
        path = "analytics/dashboards/" + self.slug + ".html"
        return [path]