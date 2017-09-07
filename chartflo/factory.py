# -*- coding: utf-8 -*-

import pandas as pd
from altair import Chart, X, Y
from .conf import HTML_TEMPLATE


class ChartController():

    def serialize_count(self, dataset, xfield, yfield, chart_type="bar", width=800, height=300, color=None, size=None):
        x = []
        y = []
        xfieldtype = xfield[1]
        yfieldtype = yfield[1]
        for datapoint in dataset:
            x.append(datapoint)
            y.append(dataset[datapoint])
        df = pd.DataFrame({xfield[0]: x, yfield[0]: y})
        xencode, yencode = self._encode_fields(xfieldtype, yfieldtype)
        chart = self._chart_class(df, chart_type).encode(x=xencode, y=yencode, color=color, size=size).configure_cell(
            width=width,
            height=height
        )
        return chart

    def serialize_timeseries(self, query, xfield, yfield, time_unit, chart_type="line", width=800, height=300, color=None, size=None):
        # print("############################## SERIALIZE TS",
        #      xfield, yfield, time_unit, )
        xfieldname = xfield[0]
        xfieldtype = xfield[1]
        #datesq = query.values(xfieldname)
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

    def serialize_filters(self, obj):
        """
        Serialize filters line protocol to a dictionary
        """
        line = obj.filters
        filters = {}
        if not line:
            dictq = {
                "app": obj.app,
                "model": obj.model,
                "filters": filters
            }
            return dictq
        if "&" in line:
            vs = line.split("&")
        else:
            vs = [line]
        for v in vs:
            vt = v.split("=")
            label = vt[0]
            val = vt[1]
            if val == "True":
                val = True
            elif val == "False":
                val = False
            filters[label] = val
        dictq = {
            "app": obj.app,
            "model": obj.model,
            "filters": filters
        }
        return dictq

    def count(self, query, field=None, func=None):
        pack = {}
        if field is not None:
            pack = {field: func}
        return self._count_for_query(query, pack)

    def _chart_class(self, df, chart_type):
        """
        returns a function to draw the right chart from string input
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
        if time_unit is not None:
            xencode = X(xfieldtype, timeUnit=time_unit)
        else:
            xencode = X(xfieldtype)
        yencode = Y(yfieldtype)
        return xencode, yencode

    def _count_for_query(self, query, fieldchecks):
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
