from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group


class Dashboard(models.Model):
    title = models.CharField(max_length=160, verbose_name=_(u"Title"))
    slug = models.CharField(max_length=120, unique=True,
                            verbose_name=_(u"Slug"))
    updated = models.DateTimeField(
        blank=True, null=True, verbose_name=_(u'Last update'))
    public = models.BooleanField(default=False, verbose_name=_(u'Public'))
    groups = models.ManyToManyField(
        Group, blank=True, verbose_name=_(u'Authorized groups'))
    icon = models.CharField(
        max_length=60, verbose_name=_(u"Icon"), default="dashboard")
    altair = models.BooleanField(default=False, verbose_name=_(
        u'Use the Altair rendering engine'))
    bokeh = models.BooleanField(default=True, verbose_name=_(
        u'Use the Bokeh rendering engine'))
    chartjs = models.BooleanField(default=True, verbose_name=_(
        u'Use the Chartjs rendering engine'))

    class Meta:
        verbose_name = _(u'Dashboard')
        verbose_name_plural = _(u'Dashboards')

    def __str__(self):
        return self.title
