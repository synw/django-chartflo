# -*- coding: utf-8 -*-


class ChartController():

    def package(self, chart_type, dataset, fields, width, height, encoding={}):
        datapack = {}
        datapack["$schema"] = "https://vega.github.io/schema/vega-lite/v2.json"
        datapack["mark"] = chart_type
        datapack["width"] = width
        datapack["height"] = height
        x, y = fields[0], fields[1]
        datapack["encoding"] = self._set_encoding(
            encoding, x, y)
        datavalues = self.serialize(dataset, x, y)
        datapack["data"] = {"values": datavalues}
        return datapack

    def serialize(self, dataset, x, y):
        datapack = []
        for datapoint in dataset:
            dataobj = {x: datapoint, y: dataset[datapoint]}
            datapack.append(dataobj)
        return datapack

    def count(self, query, field=None, func=None):
        pack = {}
        if field is not None:
            pack = {field: func}
        return self._count_for_query(query, pack)

    def _set_encoding(self, encoding, x, y):
        if encoding == {}:
            encoding["x"] = {"field": x, "type": "nominal"}
            encoding["y"] = {"field": y, "type": "quantitative"}
        return encoding

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
