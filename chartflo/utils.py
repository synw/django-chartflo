# -*- coding: utf-8 -*-


class ChartDataPack():
    
    def count_for_query(self, query, fieldpack):
        dataset = {}
        counter = 0
        for elem in query:
            commit = True
            modelname = query[0].__class__.__name__
            name = modelname
            if len(fieldpack.keys()) > 0:          
                for fieldname in fieldpack.keys():
                    name = modelname+"."+fieldname
                    fieldval = str(getattr(elem, fieldname))
                    func = fieldpack[fieldname]
                    if func is not None:
                        if func(fieldval) is False:
                            commit = False
            if commit is True:
                counter += 1
                if name in dataset.keys():
                    dataset[name] = dataset[name]+1
                else:
                    dataset[name] = 1
        return counter
    
    def package(self, chart_id, data_label, dataset, legend=False):
        return {'chart_id':chart_id, 'data_label':data_label, "dataset":dataset, "legend":legend}
    
    def count(self, query, field=None, func=None):
        pack = {}
        if field is not None:
            pack = {field:func}
        return self.count_for_query(query, pack)
        
        