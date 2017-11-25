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
