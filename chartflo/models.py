# -*- coding: utf-8 -*-

import json
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields.json import JSONField
from django.db.models.signals import post_save
from introspection.inspector import inspect
from .factory import ChartController
from goerr import err
from .signals import question_save
from .conf import CHART_TYPES, HTML_TEMPLATE


class Chart(models.Model):
    name = models.CharField(max_length=120, verbose_name=_(u"Name"))
    slug = models.CharField(max_length=120, unique=True,
                            verbose_name=_(u"Slug"))
    html = models.TextField(blank=True, verbose_name=_(u'Html'))
    json = JSONField(blank=True, verbose_name=_(
        u'Vega Lite encoded json data'))

    class Meta:
        verbose_name = _(u'Chart')
        verbose_name_plural = _(u'Charts')

    def __str__(self):
        return self.name

    def generate(self, chart, slug, name, dataset):
        """
        Generate data and save a chart object in the database
        """
        chart.name = name
        try:
            chart.json = self._patch_json(dataset.to_json())
        except Exception as e:
            err.new(e)
        try:
            chart.html = ""
            if chart.name:
                chart.html = "<h3>" + chart.name + "</h3>"
            chart.html = chart.html + self._json_to_html(slug, chart.json)
        except Exception as e:
            err.new(e)
        try:
            chart.save()
        except Exception as e:
            err.new(e)
        if err.exists:
            err.throw()

    def _patch_json(self, json_data):
        """
        Patch the Altair generated json to the newest Vega Lite spec
        """
        json_data = json.loads(json_data)
        # add schema
        json_data["$schema"] = "https://vega.github.io/schema/vega-lite/2.0.0-beta.15.json"
        # add top level width and height
        json_data["width"] = json_data["config"]["cell"]["width"]
        json_data["height"] = json_data["config"]["cell"]["height"]
        del(json_data["config"]["cell"])
        return json.dumps(json_data)

    def _json_to_html(self, slug, json_data):
        """
        Generates html from Vega lite data
        """
        html = '<div id="chart-' + slug + '"></div>'
        html += '<script>'
        html += 'var s' + slug + ' = ' + json_data + ';'
        html += 'vega.embed("#chart-' + slug + '", s' + slug + ');'
        #html += 'console.log(JSON.stringify(s{id}, null, 2));'
        html += '</script>'
        return html


class Query(models.Model):
    name = models.CharField(max_length=120, verbose_name=_(u"Name"))
    app = models.CharField(max_length=120, verbose_name=_(u"App"))
    model = models.CharField(max_length=120, verbose_name=_(u"Model"))
    filters = models.CharField(blank=True,
                               max_length=255, default="", verbose_name=_(u"Filters"))

    class Meta:
        verbose_name = _(u'Query')
        verbose_name_plural = _(u'Queries')

    def __str__(self):
        return self.name

    def count_data(self):
        """
        Returns the result of a count query from a set of filters
        """
        chart = ChartController()
        dictq = chart.serialize_filters(self)
        q, err = inspect.count(dictq)
        if err.exists:
            err.throw()
        return q

    def get_data(self):
        chart = ChartController()
        dictq = chart.serialize_filters(self)
        res, err = inspect.query(dictq)
        if err.exists:
            err.throw()
        return res


class Question(models.Model):
    name = models.CharField(max_length=120, verbose_name=_(u"Name"))
    x_field = models.CharField(
        max_length=120, verbose_name=_(u"X axis field name"))
    x_field_type = models.CharField(max_length=120, verbose_name=_(
        u"X axis field type"), help_text=_(u"Ex: 'number:Q' to declare a quantitative field"))
    y_field = models.CharField(
        max_length=120, verbose_name=_(u"Y axis field name"))
    y_field_type = models.CharField(max_length=120, verbose_name=_(
        u"Y axis field type"), help_text=_(u"Ex: 'number:Q' to declare a quantitative field"))
    # fields with defaults
    chart_type = models.CharField(
        max_length=120, choices=CHART_TYPES, default=(CHART_TYPES[0][0]), verbose_name=_(u'Chart type'))
    width = models.PositiveSmallIntegerField(blank=True,
                                             verbose_name=_(u'Width'), default=800)
    height = models.PositiveSmallIntegerField(blank=True,
                                              verbose_name=_(u'Height'), default=300)
    color = models.CharField(blank=True, max_length=120,
                             verbose_name=_(u"Color field"))
    size = models.CharField(blank=True, max_length=120,
                            verbose_name=_(u"Size field"))
    time_unit = models.CharField(
        blank=True, max_length=120, verbose_name=_(u"Time unit"))
    queries = models.ManyToManyField(Query, verbose_name=_(u"Queries"))
    html = models.TextField(blank=True, verbose_name=_(u'Html'))
    json = JSONField(blank=True, verbose_name=_(
        u'Vega Lite encoded json data'))

    class Meta:
        verbose_name = _(u'Question')
        verbose_name_plural = _(u'Questions')

    def __str__(self):
        return self.name

    def generate(self):
        """
        Generates the chart data for a question
        """
        queries = self.queries.all()
        if len(queries) == 0:
            return
        dataset = {}
        for q in queries:
            data = q.count_data()
            dataset[q.name] = data
        chart = ChartController()
        x = (self.x_field, self.x_field_type)
        y = (self.y_field, self.y_field_type)
        if self.time_unit == "":
            datapack = chart.serialize_count(
                dataset, x, y, chart_type=self.chart_type,
                width=self.width, height=self.height, color=self.color
            )
        else:
            qdata = queries[0].get_data()
            datapack = chart.serialize_timeseries(
                qdata, x, y, self.time_unit, chart_type=self.chart_type,
                width=self.width, height=self.height, color=self.color
            )
        self.json = datapack.to_json()
        self.html = datapack.to_html(
            template=HTML_TEMPLATE, id="chart_" + str(self.id))
        post_save.disconnect(question_save, sender=Question)
        self.save()
        post_save.connect(question_save, sender=Question)


class Dashboard(models.Model):
    title = models.CharField(max_length=120, verbose_name=_(u"Title"))
    slug = models.CharField(max_length=120, unique=True,
                            verbose_name=_(u"Slug"))
    questions = models.ManyToManyField(
        Question, blank=True, verbose_name=_(u"Questions"))
    charts = models.ManyToManyField(
        Chart, blank=True, verbose_name=_(u"Charts"))

    class Meta:
        verbose_name = _(u'Dashboard')
        verbose_name_plural = _(u'Dashboards')

    def __str__(self):
        return self.title


post_save.connect(question_save, sender=Question)
