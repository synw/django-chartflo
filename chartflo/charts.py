# -*- coding: utf-8 -*-
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.io import export_png
from django.utils._os import safe_join
from django.conf import settings


def export(plot, filename):
    path = safe_join(settings.BASE_DIR + "/media/charts", filename)
    export_png(plot, filename="plot.png")


def bar_chart(data):
    x = []
    y = []
    for datapoint in data:
        x.append(datapoint)
        y.append(data[datapoint])
    print(x, y)

    source = ColumnDataSource(dict(x=x, y=y))

    p = figure(plot_width=400, plot_height=400, x_range=source.data["x"],)
    p.vbar(source=source, x=x, top='y',
           width=0.5, bottom=0, color="firebrick")
    script, div = components(p)

    #export_png(p, filename="plot.png")
    #export(p, "users.png")

    return script, div
