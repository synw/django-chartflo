# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.http.response import Http404
from django.template.loader import get_template
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from chartflo.models import Dashboard


class DashboardView(TemplateView):
    """
    Generic dashboard view
    """
    template_name = "dashboards/index.html"

    def dispatch(self, request, *args, **kwargs):
        slug = kwargs["slug"]
        self.dashboard = get_object_or_404(
            Dashboard.objects.prefetch_related("groups"), slug=slug)
        groups = self.dashboard.groups.all()
        user_groups = request.user.groups.all()
        authorized = False
        for group in groups:
            if group in user_groups or request.user.is_superuser is True:
                authorized = True
                break
        if authorized is False:
            raise Http404
        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        t = get_template("dashboards/" + self.dashboard.slug + ".html")
        try:
            t = get_template("dashboards/sidebars/" +
                             self.dashboard.slug + ".html")
            sidebar = t.render({})
        except Exception as e:
            raise(e)
        context["dashboard"] = self.dashboard
        context["sidebar"] = sidebar
        return context


def getDashboardPageView(request, slug):
    """
    Loads a dashboard's content
    """
    if not request.user.is_superuser is True:
        raise Http404
    t = get_template("dashboards/" + slug + ".html")
    html = t.render({"slug": slug})
    return HttpResponse(html)
