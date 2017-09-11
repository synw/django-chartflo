# -*- coding: utf-8 -*-

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
import html

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

TO_HTML = getattr(settings, 'CHARTFLO_TO_HTML', False)

HTML_TEMPLATE = """
<div id="{id}"></div>
<script>
var s{id} = patch_spec({spec});
s{id}.$schema = "https://vega.github.io/schema/vega-lite/2.0.0-beta.15.json";
vega.embed("#{id}", s{id});
console.log(JSON.stringify(s{id}, null, 2));
</script>
"""


def number_template(number, legend=None):
    res = '<div class="panel-number"><h1>' + str(number) + "</h1>"
    if legend is not None:
        res = res + '<div class="panel-legend">' + legend + '</div>'
    res = res + "</div>"
    return res
