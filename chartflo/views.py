# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.http.response import Http404
from django.template.loader import get_template
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Dashboard


def check_groups(dashboard, request):
    """
    Check groups authorization for a dashboard
    """
    if dashboard.public is True:
        return True
    if request.user.is_superuser is True:
        return True
    groups = dashboard.groups.all()
    user_groups = request.user.groups.all()
    for group in groups:
        if group in user_groups:
            return True
    return False


class DashboardView(TemplateView):
    """
    Generic dashboard view
    """

    def dispatch(self, request, *args, **kwargs):
        slug = kwargs["dashboard_name"]
        self.dashboard = get_object_or_404(
            Dashboard.objects.prefetch_related("groups"), slug=slug)
        authorized = check_groups(self.dashboard, request)
        if authorized is False:
            raise Http404
        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context["dashboard"] = self.dashboard.slug
        context["icon"] = self.dashboard.icon
        context["altair"] = self.dashboard.altair
        context["bokeh"] = self.dashboard.bokeh
        context["chartjs"] = self.dashboard.chartjs
        return context

    def get_template_names(self):
        template_name = "dashboards/" + self.dashboard.slug + "/index.html"
        return [template_name]


def getDashboardPageView(request, dashboard_name, page_name):
    """
    Loads a dashboard's page content
    """
    if "__" in page_name:
        page_name = page_name.replace("__", "/")
    dashboard = get_object_or_404(
        Dashboard.objects.prefetch_related("groups"), slug=dashboard_name)
    authorized = check_groups(dashboard, request)
    if authorized is False:
        raise Http404
    t = get_template("dashboards/" + dashboard_name +
                     '/' + page_name + ".html")
    html = t.render({"page": page_name, "dashboard": dashboard.slug})
    return HttpResponse(html)


def getDashboardIndexView(request, dashboard_name):
    """
    Loads a dashboard's frontpage
    """
    return getDashboardPageView(request, dashboard_name, "index")
