# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from introspection.inspector import inspect
from chartflo.serializers import q_to_dictq


class Filter(models.Model):
    name = models.CharField(max_length=120, verbose_name=_(u"Name"))
    value = models.CharField(max_length=255, verbose_name=_(u"Value"))

    class Meta:
        verbose_name = _(u'Filter')
        verbose_name_plural = _(u'Filters')

    def __str__(self):
        return self.name


class Query(models.Model):
    name = models.CharField(max_length=120, verbose_name=_(u"Name"))
    app = models.CharField(max_length=120, verbose_name=_(u"App"))
    model = models.CharField(max_length=120, verbose_name=_(u"Model"))
    filters = models.ManyToManyField(
        Filter, blank=True, verbose_name=_(u"Filters"), related_name="queries")

    class Meta:
        verbose_name = _(u'Query')
        verbose_name_plural = _(u'Queries')

    def __str__(self):
        return self.name

    def count_data(self):
        filtersq = self.filters.all()
        dictq = q_to_dictq(self, filtersq)
        q = inspect.count(dictq)
        return q


class Question(models.Model):
    name = models.CharField(max_length=120, verbose_name=_(u"Name"))
    queries = models.ManyToManyField(
        Query, verbose_name=_(u"Queries"), related_name="questions")
    html = models.TextField(blank=True, verbose_name=_(u'Html'))
    script = models.TextField(blank=True, verbose_name=_(u'Script'))

    class Meta:
        verbose_name = _(u'Question')
        verbose_name_plural = _(u'Questions')

    def __str__(self):
        return self.name


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
