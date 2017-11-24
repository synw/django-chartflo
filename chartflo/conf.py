# -*- coding: utf-8 -*-

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

CHART_TYPES = (
    ("bar", _(u"Bar")),
    ("line", _(u"Line")),
    ("circle", _(u"Circle")),
    ("point", _(u"Point")),
    ("square", _(u"Square")),
    ("tick", _(u"Tick")),
    ("text", _(u"Text")),
)

ENGINE = getattr(settings, 'CHARTFLO_ENGINE', "vegalite")


def number_template(number, legend=None, unit="", thresholds={}, icon=None, color="green"):
    if icon is None:
        icon = '<span class="info-box-icon"><i class="fa fa-thumbs-o-up"></i></span>'
    else:
        icon = '<span class="info-box-icon"><i class="fa fa-' + icon + '"></i></span>'
    if unit != "":
        unit = '<span class="unit">&nbsp;' + unit + '</span>'
    css_class = ""
    if thresholds:
        if "low" in thresholds:
            if number <= thresholds["low"]:
                css_class = "low"
        if "high" in thresholds:
            if number >= thresholds["high"]:
                css_class = "high"
    wrapper = '<div class="info-box bg-' + color + '">'
    res = wrapper + icon + '\n<div class="info-box-content">'
    if legend is not None:
        res = res + '\n<span class="info-box-text ' + \
            css_class + '">' + legend + '</span>'
    res = res + '\n<span class="info-box-number">' + \
        str(number) + ' ' + unit + '</span>'
    res = res + "\n</div></div>"
    return res
