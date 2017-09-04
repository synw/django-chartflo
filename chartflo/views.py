# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from .conf import ENGINE


class ChartsView(TemplateView):
    template_name = 'chartflo/charts.html'
    chart_type = "bar"
    title = ""
    engine = ENGINE
    x = ()
    y = ()
    width = 800
    height = 300
    time_unit = ""

    def get_data(self):
        return {}

    def get_context_data(self, **kwargs):
        context = super(ChartsView, self).get_context_data(**kwargs)
        # get data
        datapack = self.get_data()
        # context
        context['datapack'] = datapack.to_json()
        context["title"] = self.title
        context["chart_id"] = "chart"
        context["chart_url"] = self._get_template_url()
        return context

    def _get_template_url(self):
        if self.engine == "vegalite":
            url = "chartflo/vegalite/chart.html"
        else:
            url = "chartflo/" + self.engine + "/" + self.chart_type + ".html"
        return url
