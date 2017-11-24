# -*- coding: utf-8 -*-

from goerr import err
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from gencharts import ChartsGenerator
from .utils import _write_file
from .conf import number_template


class Dashboard(models.Model):
    slug = models.CharField(max_length=120, unique=True,
                            verbose_name=_(u"Slug"))
    title = models.CharField(max_length=160, verbose_name=_(u"Title"))
    updated = models.DateTimeField(
        blank=True, null=True, verbose_name=_(u'Last update'))
    groups = models.ManyToManyField(
        Group, blank=True, verbose_name=_(u'Authorized groups'))
    icon = models.CharField(
        max_length=60, verbose_name=_(u"Icon"), default="dashboard")

    class Meta:
        verbose_name = _(u'Dashboard')
        verbose_name_plural = _(u'Dashboards')

    def __str__(self):
        return self.title


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

    def generate(self, dashboard=None, color="green", icon=None):
        """
        Generate data and save a panel number object in the database
        """
        html = number_template(self.value, self.legend,
                               self.unit, self.thresholds, icon, color)
        self.html = html
        self.updated = timezone.now()
        self.save()
        _write_file(self.slug, self.html, "number", dashboard=dashboard)
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

    def record(self, chart, slug, name="", generator="",
               modelnames="", html_before="", html_after=""):
        """
        Generate data and save a chart object in the database
        """
        dataset = chart.to_json()
        self.json = {}
        try:
            self.json = self._patch_json(dataset)
        except Exception as e:
            err.new(e)
        try:
            self.html = ""
            if self.name:
                self.html = "<h3>" + name + "</h3>"
            self.html = html_before + self._json_to_html(slug, self.json) +\
                self._json_to_html(slug, self.json) + html_after
        except Exception as e:
            err.new(e)
        self.generator = generator
        self.modelnames = modelnames
        # save to db
        try:
            self.save()
        except Exception as e:
            err.new(e)
