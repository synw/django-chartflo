# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields.json import JSONField
from django.db.models.signals import post_save
from introspection.inspector import inspect
from .factory import ChartController
from .signals import question_save
from .conf import CHART_TYPES, HTML_TEMPLATE


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
        q = inspect.count(dictq)
        return q

    def get_data(self):
        chart = ChartController()
        dictq = chart.serialize_filters(self)
        res, err = inspect.query(dictq)
        if err.exists:
            err.trace()
        print("RES", res)
        return res


class Question(models.Model):
    name = models.CharField(max_length=120, verbose_name=_(u"Name"))
    queries = models.ManyToManyField(
        Query, verbose_name=_(u"Queries"), related_name="questions")
    html = models.TextField(blank=True, verbose_name=_(u'Html'))
    script = models.TextField(blank=True, verbose_name=_(u'Script'))
    json = JSONField(blank=True, verbose_name=_(
        u'Vega Lite encoded json data'))
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

    class Meta:
        verbose_name = _(u'Question')
        verbose_name_plural = _(u'Questions')

    def __str__(self):
        return self.name

    def generate(self):
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
        Question, verbose_name=_(u"Questions"), related_name="dashboards")

    class Meta:
        verbose_name = _(u'Dashboard')
        verbose_name_plural = _(u'Dashboards')

    def __str__(self):
        return self.title


post_save.connect(question_save, sender=Question)
