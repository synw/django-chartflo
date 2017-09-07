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

HTML_TEMPLATE = """
<div id="{id}"></div>
<script>
var s{id} = patch_spec({spec});
s{id}.$schema = "https://vega.github.io/schema/vega-lite/2.0.0-beta.15.json";
vega.embed("#{id}", s{id});
console.log(JSON.stringify(s{id}, null, 2));
</script>
"""
