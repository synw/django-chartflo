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

TO_HTML = getattr(settings, 'CHARTFLO_TO_HTML', True)
TO_JSON = getattr(settings, 'CHARTFLO_TO_JSON', False)


def number_template(number, legend=None, unit=""):
    if unit != "":
        unit = '<span class="unit">&nbsp;' + unit + '</span>'
    res = '<div class="panel-number"><h1>' + str(number) + unit + "</h1>"
    if legend is not None:
        res = res + '<div class="panel-legend">' + legend + '</div>'
    res = res + "</div>"
    return res
