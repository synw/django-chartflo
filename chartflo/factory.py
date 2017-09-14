# -*- coding: utf-8 -*-

import pandas as pd
from altair import Chart, X, Y
from blessings import Terminal
from .models import Chart as ChartFlo


COLOR = Terminal()
OK = "[" + COLOR.bold_green("ok") + "] "


class ChartController():
    """
    Charts builder: handles serialization into Vega Lite format
    """

    def serialize_count(self, dataset, xfield, yfield, chart_type="bar",
                        width=800, height=300, color=None, size=None):
        """
        Serialize a chart from a count dataset:
        Ex: {"users":200, "groups":30}
        """
        x = []
        y = []
        xfieldtype = xfield[1]
        yfieldtype = yfield[1]
        for datapoint in dataset:
            x.append(datapoint)
            y.append(dataset[datapoint])
        df = pd.DataFrame({xfield[0]: x, yfield[0]: y})
        xencode, yencode = self._encode_fields(xfieldtype, yfieldtype)
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

    def serialize_timeseries(self, query, xfield, yfield, time_unit,
                             chart_type="line", width=800,
                             height=300, color=None, size=None):
        """
        Serialize a timeseries chart from a query
        """
        xfieldname = xfield[0]
        xfieldtype = xfield[1]
        dates = []
        vals = []
        yfieldname = yfield[0]
        yfieldtype = yfield[1]
        for row in query:
            # date
            has_date = False
            d = getattr(row, xfieldname)
            if d is not None:
                dstr = d.strftime("%Y-%m-%d %H:%M:%S")
                dates.append(dstr)
                has_date = True
            if has_date is True:
                v = getattr(row, yfieldname)
                vals.append(v)
        df = pd.DataFrame({xfieldname: dates, yfieldname: vals})
        # print(df)
        xencode, yencode = self._encode_fields(
            xfieldtype, yfieldtype, time_unit)
        print("COL", color)
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
                bandSize=30
            )
        return chart

    def count(self, query, field=None, func=None):
        """
        Count values for a query doing custom checks on fields
        """
        pack = {}
        if field is not None:
            pack = {field: func}
        return self._count_for_query(query, pack)

    def generate(self, slug, name, chart_type, query, x, y,
                 width, height, time_unit=None, color=None,
                 size=None, verbose=False):
        """
        Generates or update a chart instance from a query
        """
        global OK, COLOR
        if verbose is True:
            print("Serializing", slug, "chart...")
        chart = ChartController()
        if time_unit is not None:
            dataset = chart.serialize_timeseries(
                query, x, y, time_unit=time_unit, chart_type=chart_type,
                width=width, height=height, size=size, color=color
            )
        else:
            dataset = chart.serialize_count(
                query, x, y, chart_type=chart_type,
                width=width, height=height, size=size, color=color
            )
        chart, _ = ChartFlo.objects.get_or_create(slug=slug)
        chart.generate(chart, slug, name, dataset)
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

    def _encode_fields(self, xfieldtype, yfieldtype, time_unit=None):
        """
        Encode the fields in Altair format
        """
        if time_unit is not None:
            xencode = X(xfieldtype, timeUnit=time_unit)
        else:
            xencode = X(xfieldtype)
        yencode = Y(yfieldtype)
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
