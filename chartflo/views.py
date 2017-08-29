# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from .factory import ChartDataPack
from .conf import ENGINE


class ChartsView(TemplateView):
    template_name = 'chartflo/charts.html'
    chart_type = "pie"
    title = ""
    engine = ENGINE

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
