# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from chartflo.factory import ChartDataPack


class ChartsView(TemplateView):
    template_name = 'chartflo/charts.html'
    graph_type = "pie"
    title = ""

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
        context["graph_type"] = self.graph_type
        context["title"] = context["label"] = self.title
        context["chart_url"] = self._get_chart_url()
        return context

    def _get_chart_url(self):
        url = "chartflo/charts/" + self.graph_type + ".html"
        return url
