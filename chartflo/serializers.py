# -*- coding: utf-8 -*-


def q_to_dictq(obj, filtersq):
    filters = {}
    for f in filtersq:
        if "&" in f.value:
            vs = f.value.split("&")
        else:
            vs = [f.value]
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
