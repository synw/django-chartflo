# -*- coding: utf-8 -*-

import json
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from goerr import err
from gencharts import ChartsGenerator
from .utils import _write_file
from .conf import number_template


class Number(models.Model):
    slug = models.CharField(max_length=120, unique=True,
                            verbose_name=_(u"Slug"))
    value = models.IntegerField(verbose_name=_(u"Value"), default=0)
    unit = models.CharField(max_length=120, blank=True,
                            verbose_name=_(u"Unit"))
    legend = models.CharField(
        max_length=120, blank=True, verbose_name=_(u'Legend'))
    html = models.TextField(blank=True, verbose_name=_(u'Html'))
    updated = models.DateTimeField(
        blank=True, null=True, verbose_name=_(u'Last update'))
    modelnames = models.CharField(max_length=200, blank=True,
                                  verbose_name=_(u"Associated models"),
                                  help_text="List of model names: ex: User,Group"
                                  )
    generator = models.CharField(
        max_length=120, blank=True, verbose_name=_(u"Generator"))
    thresholds = models.CharField(max_length=255, blank=True,
                                  verbose_name=_(u"Thresholds"))

    class Meta:
        verbose_name = _(u'Number')
        verbose_name_plural = _(u'Numbers')

    def __str__(self):
        return self.legend

    def generate(self):
        """
        Generate data and save a panel number object in the database
        """
        html = number_template(self.value, self.legend,
                               self.unit, self.thresholds)
        self.html = html
        self.updated = timezone.now()
        self.save()
        _write_file(self.slug, self.html, "number")
        if err.exists:
            if settings.DEBUG is True:
                err.trace()
            else:
                err.throw()


class Chart(models.Model, ChartsGenerator):
    name = models.CharField(max_length=120, verbose_name=_(u"Name"))
    slug = models.CharField(max_length=120, unique=True,
                            db_index=True, verbose_name=_(u"Slug"))
    html = models.TextField(blank=True, verbose_name=_(u'Html'))
    json = models.TextField(blank=True, verbose_name=_(
        u'Vega Lite encoded json data'))
    html_before = models.TextField(blank=True, verbose_name=_(u'Html before'))
    html_after = models.TextField(blank=True, verbose_name=_(u'Html after'))
    updated = models.DateTimeField(
        blank=True, null=True, verbose_name=_(u'Last update'))
    modelnames = models.CharField(max_length=200, blank=True,
                                  verbose_name=_(u"Associated models"),
                                  help_text="List of model names: ex: User,Group"
                                  )
    generator = models.CharField(
        max_length=120, blank=True, verbose_name=_(u"Generator"))

    class Meta:
        verbose_name = _(u'Chart')
        verbose_name_plural = _(u'Charts')

    def __str__(self):
        return self.name

    def generate(self, chart, slug, name, dataset, generator="",
                 modelnames="", html_before="", html_after=""):
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
            chart.html = html_before + chart.html +\
                self._json_to_html(slug, chart.json) + html_after
        except Exception as e:
            err.new(e)
        chart.generator = generator
        chart.modelnames = modelnames
        # save to db
        try:
            chart.save()
        except Exception as e:
            err.new(e)
