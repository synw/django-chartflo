# -*- coding: utf-8 -*-
from collections import OrderedDict
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
    template_name = "chartflo/dashboards/index.html"

    def dispatch(self, request, *args, **kwargs):
        slug = kwargs["dashboard_name"]
        self.dashboard = get_object_or_404(
            Dashboard.objects.prefetch_related("groups", 'views'), slug=slug)
        authorized = check_groups(self.dashboard, request)
        if authorized is False:
            raise Http404
        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context["dashboard_slug"] = self.dashboard.slug
        context["icon"] = self.dashboard.icon
        context["altair"] = self.dashboard.altair
        context["bokeh"] = self.dashboard.bokeh
        context["chartjs"] = self.dashboard.chartjs
        context["title"] = self.dashboard.title
        context["navbar_class"] = self.dashboard.navbar_class
        content_template = "chartflo/dashboards/content.html"
        if self.dashboard.custom_content == True:
            content_template = "dashboards/" + self.dashboard.slug + "/content.html"
        context["dashboard_content_template"] = content_template
        header = "chartflo/dashboards/header.html"
        if self.dashboard.custom_header is True:
            header = "dashboards/" + self.dashboard.slug + "/header.html"
        context["dashboard_header_template"] = header
        viewsq = self.dashboard.views.all().order_by("order")
        views_templates = {}
        views_titles = OrderedDict()
        active_view = None
        for view in viewsq:
            views_templates[view.slug] = "dashboards/" + self.dashboard.slug + \
                "/views/" + view.slug + ".html"
            views_titles[view.slug] = view.title
            if view.active == True:
                active_view = view.slug
        context["views_templates"] = views_templates
        context["views_titles"] = views_titles
        context["active_view"] = active_view
        return context


def getDashboardView(request, dashboard_name, view_name):
    """
    Loads a dashboard's view
    """
    dashboard = get_object_or_404(
        Dashboard.objects.prefetch_related("groups"), slug=dashboard_name)
    authorized = check_groups(dashboard, request)
    if authorized is False:
        raise Http404
    t = get_template("dashboards/" + dashboard_name + 
                     '/views/' + view_name + ".html")
    html = t.render()
    return HttpResponse(html)
