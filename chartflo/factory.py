# -*- coding: utf-8 -*-

import pandas as pd
from altair import Chart, X, Y, Axis
from blessings import Terminal
from django.db.models.query import QuerySet
from .models import Chart as ChartFlo, Number


COLOR = Terminal()
OK = "[" + COLOR.bold_green("ok") + "] "


class ChartController():
    """
    Charts builder: handles serialization into Vega Lite format
    """

    def serialize_from_dataset(self, dataset, xfield, yfield, chart_type="bar",
                               width=800, height=300, color=None, size=None):
        """
        Serialize a chart from a count dataset:
        Ex: {"users":200, "groups":30}
        """
        x = []
        y = []
        for datapoint in dataset:
            x.append(datapoint)
            y.append(dataset[datapoint])
        df = pd.DataFrame({xfield[0]: x, yfield[0]: y})
        xencode, yencode = self._encode_fields(xfield, yfield)
        chart = self._chart_class(df, chart_type).encode(
            x=xencode,
            y=yencode,
            color=color,
            size=size
        ).configure_cell(
            width=width,
            height=height
        )
        return chart

    def serialize_series_from_altairdata(self, dataset, xfield, yfield, time_unit,
                                         chart_type="line", width=800,
                                         height=300, color=None, size=None):
        """
        Serialize a timeseries from a dataset
        """
        xencode, yencode = self._encode_fields(
            xfield, yfield, time_unit)
        chart = self._chart_class(dataset, chart_type).encode(
            x=xencode,
            y=yencode,
            color=color,
            size=size,
        ).configure_cell(
            width=width,
            height=height
        ).configure_scale(
            bandSize=30
        )
        return chart

    def serialize_series_from_query(self, query, xfield, yfield, time_unit,
                                    chart_type="line", width=800,
                                    height=300, color=None, size=None):
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
            xfield, yfield, time_unit)
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
            ).configure_scale(
                bandSize=10
            )
        return chart

    def serialize_date(self, date):
        """
        Serializes a datetime object to Vega Lite format
        """
        return date.strftime("%Y-%m-%d %H:%M:%S")

    def count(self, query, field=None, func=None):
        """
        Count values for a query doing custom checks on fields
        """
        pack = {}
        if field is not None:
            pack = {field: func}
        return self._count_for_query(query, pack)

    def generate_series(self, slug, name, chart_type, datapack, x, y, width, height,
                        generator, time_unit=None, color=None,
                        size=None, verbose=False, modelnames=""):
        if not isinstance(datapack, QuerySet):
            dataset = self.serialize_series_from_altairdata(
                datapack, x, y, time_unit=time_unit, chart_type=chart_type,
                width=width, height=height, size=size, color=color
            )
        else:
            dataset = self.serialize_series_from_query(
                datapack, x, y, time_unit=time_unit, chart_type=chart_type,
                width=width, height=height, size=size, color=color
            )
        chart, _ = ChartFlo.objects.get_or_create(slug=slug)
        chart.generate(chart, slug, name, dataset, modelnames, generator)
        if verbose is True:
            print(OK + "Chart", COLOR.bold(slug), "saved")

    def generate(self, slug, name, chart_type, query, x, y, width, height,
                 generator, color=None,
                 size=None, verbose=False, modelnames=""):
        """
        Generates or update a chart instance from a query
        """
        global OK, COLOR
        if verbose is True:
            print("Serializing", slug, "chart...")
        dataset = self.serialize_from_dataset(
            query, x, y, chart_type=chart_type,
            width=width, height=height, size=size, color=color
        )
        chart, _ = ChartFlo.objects.get_or_create(slug=slug)
        chart.generate(chart, slug, name, dataset, generator, modelnames)
        if verbose is True:
            print(OK + "Chart", COLOR.bold(slug), "saved")

    def _chart_class(self, df, chart_type):
        """
        Get the right chart class from a string
        """
        if chart_type == "bar":
            return Chart(df).mark_bar()
        elif chart_type == "circle":
            return Chart(df).mark_circle()
        elif chart_type == "line":
            return Chart(df).mark_line()
        elif chart_type == "point":
            return Chart(df).mark_point()
        elif chart_type == "area":
            return Chart(df).mark_area()
        elif chart_type == "tick":
            return Chart(df).mark_tick()
        elif chart_type == "text":
            return Chart(df).mark_text()
        elif chart_type == "square":
            return Chart(df).mark_square()
        elif chart_type == "rule":
            return Chart(df).mark_rule()
        return None

    def _encode_fields(self, xfield, yfield, time_unit=None):
        """
        Encode the fields in Altair format
        """
        xfieldtype = xfield[1]
        yfieldtype = yfield[1]
        x_options = None
        if len(xfield) > 2:
            x_options = xfield[2]
        y_options = None
        if len(yfield) > 2:
            y_options = yfield[2]
        if time_unit is not None:
            if x_options is None:
                xencode = X(xfieldtype, timeUnit=time_unit)
            else:
                xencode = X(
                    xfieldtype,
                    axis=Axis(**x_options),
                    timeUnit=time_unit
                )
        else:
            if x_options is None:
                xencode = X(xfieldtype)
            else:
                xencode = X(
                    xfieldtype,
                    axis=Axis(**x_options)
                )
        if y_options is None:
            yencode = Y(yfieldtype)
        else:
            yencode = Y(
                yfieldtype,
                axis=Axis(**y_options)
            )
        return xencode, yencode

    def _count_for_query(self, query, fieldchecks):
        """
        Do custom checks on fields and returns a count
        """
        counter = 0
        for obj in query:
            commit = True
            if len(fieldchecks.keys()) > 0:
                for fieldname in fieldchecks.keys():
                    fieldval = str(getattr(obj, fieldname))
                    func = fieldchecks[fieldname]
                    if func is not None:
                        if func(fieldval) is False:
                            commit = False
            if commit is True:
                counter += 1
        return counter


class NumberController():

    def generate(self, slug, legend, value, generator, unit="", verbose=False, modelnames=""):
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
            num.save()
        num.generate()
        if verbose is True:
            print("[x] Generated number", legend)
