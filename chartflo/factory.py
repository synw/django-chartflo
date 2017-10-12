# -*- coding: utf-8 -*-

import pandas as pd
from altair import Scale
from blessings import Terminal
from django.db.models.query import QuerySet
from django.utils._os import safe_join
from django.conf import settings
from goerr import err
from gencharts import ChartsGenerator
from .models import Chart as ChartFlo, Number


COLOR = Terminal()
OK = "[" + COLOR.bold_green("ok") + "] "


class ChartController(ChartsGenerator):
    """
    Charts builder: handles serialization into Vega Lite format
    """

    def serialize_query(self, query, xfield, yfield, time_unit,
                        chart_type="line", width=800,
                        height=300, color=None, size=None,
                        scale=Scale(zero=False)):
        """
        Serialize a timeseries chart from a query
        """
        xfieldname = xfield[0]
        dates = []
        vals = []
        yfieldname = yfield[0]
        for row in query:
            # date
            has_date = False
            d = getattr(row, xfieldname)
            if d is not None:
                dstr = self.serialize_date(d)
                dates.append(dstr)
                has_date = True
            if has_date is True:
                v = getattr(row, yfieldname)
                vals.append(v)
        df = pd.DataFrame({xfieldname: dates, yfieldname: vals})
        # print(df)
        xencode, yencode = self._encode_fields(
            xfield, yfield, time_unit, scale=scale)
        if chart_type != "tick":
            chart = self._chart_class(df, chart_type).encode(
                x=xencode,
                y=yencode,
                color=color,
                size=size,
            ).configure_cell(
                width=width,
                height=height
            )
        else:
            chart = self._chart_class(df, chart_type).encode(
                x=xencode,
                color=color,
                size=size,
            ).configure_cell(
                width=width,
                height=height
            )
        return chart

    def generate(self, slug, name, chart_type, datapack, x, y, width, height,
                 generator, time_unit=None, color=None,
                 size=None, verbose=False, modelnames="",
                 scale=Scale(zero=False)):
        """
        Generates a chart from either a Django orm query, a pandas dataframe, a dictionnary
        or an Altair Data object
        """
        if not isinstance(datapack, QuerySet):
            dataset = self.serialize(
                datapack, x, y, time_unit=time_unit, chart_type=chart_type,
                width=width, height=height, size=size, color=color,
                scale=scale
            )
        else:
            dataset = self.serialize_query(
                datapack, x, y, time_unit=time_unit, chart_type=chart_type,
                width=width, height=height, size=size, color=color,
                scale=scale
            )
        chart, _ = ChartFlo.objects.get_or_create(slug=slug)
        folderpath = safe_join(settings.BASE_DIR, "templates/chartflo")
        self.html(slug, name, dataset, folderpath)
        chart.generate(chart, slug, name, dataset)
        if verbose is True:
            print(OK + "Chart", COLOR.bold(slug), "saved")
        if err.exists:
            err.report()


class NumberController():

    def generate(self, slug, legend, value, generator, unit="",
                 verbose=False, modelnames="", thresholds={}):
        """
        Create or update a number instance from a value
        """
        defaults = {"legend": legend, "value": value, "unit": unit}
        num, created = Number.objects.get_or_create(
            slug=slug, defaults=defaults)
        if created is False:
            num.legend = legend
            num.value = value
            num.unit = unit
            num.generator = generator
            num.modelnames = modelnames
            num.thresholds = thresholds
            num.save()
        num.generate()
        if verbose is True:
            print("[x] Generated number", legend)
