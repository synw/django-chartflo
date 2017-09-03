# -*- coding: utf-8 -*-

import pandas as pd
#from django_pandas.io import read_frame
from altair import Chart


class ChartController():

    def serialize_count(self, dataset, xfield, yfield, chart_type="bar", width=800, height=300):
        x = []
        y = []
        for datapoint in dataset:
            x.append(datapoint)
            y.append(dataset[datapoint])
        df = pd.DataFrame({xfield[0]: x, yfield[0]: y})
        xencode = xfield[0] + ":" + xfield[1]
        yencode = yfield[0] + ":" + yfield[1]
        chart = Chart(df).mark_bar().encode(x=xencode, y=yencode)
        datapack = chart.to_dict()
        datapack["$schema"] = "https://vega.github.io/schema/vega-lite/v2.json"
        datapack["width"] = width
        datapack["height"] = height
        datapack["mark"] = chart_type
        return datapack

    """
    # TODO
    def serialize_query(self, chart_type, queries, width, height):
        dfs = []
        for query in queries:
            df = read_frame(query.values("username"))
            dfs.append(df)
        print(df)
        chart = Chart(df).mark_point().encode(x="a:N", y="b:Q")
        return chart
    """

    def count(self, query, field=None, func=None):
        pack = {}
        if field is not None:
            pack = {field: func}
        return self._count_for_query(query, pack)

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
