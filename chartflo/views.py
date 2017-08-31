# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.http.response import Http404
from chartflo.factory import ChartDataPack
from chartflo.models import Dashboard


class DashboardView(TemplateView):
    template_name = "chartflo/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        dashboard = None
        try:
            dashboard = Dashboard.objects.get(slug=kwargs["slug"])
        except:
            Http404()
        questions = dashboard.questions.all()
        html = ""
        for question in questions:
            html = html + question.script + question.html
        context["html_data"] = html
        context["title"] = dashboard.title
        return context


class ChartsView(TemplateView):
    template_name = 'chartflo/charts.html'
    chart_type = "pie"
    title = ""
    engine = "amcharts"

    def get_data(self):
        return {}

    def get_context_data(self, **kwargs):
        context = super(ChartsView, self).get_context_data(**kwargs)
        # get data
        P = ChartDataPack()
        dataset = self.get_data()
        # package the data
        datapack = P.package("chart_id", self.title, dataset)
        # options
        datapack['legend'] = True
        datapack['export'] = False
        context['datapack'] = datapack
        context["title"] = context["label"] = self.title
        context["chart_url"] = self._get_template_url()
        return context

    def _get_template_url(self):
        url = "chartflo/" + self.engine + "/" + self.chart_type + ".html"
        return url
