# -*- coding: utf-8 -*-


class ChartController():

    def package(self, chart_id, data_label, dataset, legend=False):
        return {'chart_id': chart_id, 'data_label': data_label, "dataset": dataset, "legend": legend}

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