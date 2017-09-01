# -*- coding: utf-8 -*-
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import TemplateView
from .factory import ChartController
from .conf import ENGINE


class ChartsView(TemplateView):
    template_name = 'chartflo/charts.html'
    chart_type = "bar"
    title = ""
    engine = ENGINE
    fields = []
    width = 800
    height = 300

    def get_data(self):
        return {}

    def get_context_data(self, **kwargs):
        context = super(ChartsView, self).get_context_data(**kwargs)
        # get data
        chart = ChartController()
        dataset = self.get_data()
        # package the data
        datapack = chart.package(
            self.chart_type, dataset, self.fields, self.width, self.height)
        # options
        #print("DUMP", json.dumps(datapack, cls=DjangoJSONEncoder, indent=2))
        context['datapack'] = json.dumps(
            datapack, cls=DjangoJSONEncoder)
        context["title"] = context["label"] = self.title
        context["chart_id"] = "chart"
        context["chart_url"] = self._get_template_url()
        return context

    def _get_template_url(self):
        if self.engine == "vegalite":
            url = "chartflo/vegalite/chart.html"
        else:
            url = "chartflo/" + self.engine + "/" + self.chart_type + ".html"
        return url
