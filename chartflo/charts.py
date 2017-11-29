import pandas as pd
from goerr import err
from dataswim import ds
from django.db.models.query import QuerySet


class Chart():
    """
    Class to handle charts
    """

    def __init__(self):
        """
        Set a default rendering engine
        """
        self.engine = "bokeh"
        self.opts = dict(width=940)
        self.style = dict(color="blue")

    def convert_dataset(self, dataset, x=None, y=None):
        """
        Convert the input data to pandas dataframe
        """
        if type(x) == tuple:
            x = x[0]
        if type(y) == tuple:
            y = y[0]
        try:
            self._check_fields(x, y)
        except Exception as e:
            err.new(e, self.convert_dataset, "Can not find fields", x, y)
            err.throw()
        try:
            if isinstance(dataset, pd.DataFrame):
                return dataset
            elif isinstance(dataset, QuerySet):
                x_vals = []
                y_vals = []
                for row in list(dataset.values()):
                    try:
                        y_vals.append(row[y])
                    except:
                        y_vals.append(1)
                    x_vals.append(row[x])
                dataset = pd.DataFrame({x: x_vals, y: y_vals})
            elif isinstance(dataset, dict):
                dataset = self._dict_to_df(dataset, x, y)
            elif isinstance(dataset, list):
                return pd.DataFrame(dataset)
            else:
                err.new(self.convert_dataset,
                        "Data format unknown: "
                        + str(type(dataset)) +
                        " please provide a dictionnary, a Django Queryset or a Pandas DataFrame")
                err.throw()
        except Exception as e:
            err.new(e, self.convert_dataset, "Can not convert dataset")
            err.throw()
        return dataset

    def _check_fields(self, x, y):
        """
        Check if X and Y field are set
        """
        if x is None:
            if ds.x is None:
                err.new(self._check_fields,
                        "No X field set: please pass one as parameter")
                return
            ds.x = x
        if y is None:
            if ds.y is None:
                err.new(self._check_fields,
                        "No Y field set: please pass one as parameter")
            ds.y = y

    def _dict_to_df(self, dictobj, xfield, yfield):
        """
        Converts a dictionnary to a pandas dataframe
        """
        x = []
        y = []
        for datapoint in dictobj:
            x.append(datapoint)
            y.append(dictobj[datapoint])
        if type(xfield) == tuple:
            xfield = xfield[0]
        if type(yfield) == tuple:
            yfield = yfield[0]
        df = pd.DataFrame({xfield: x, yfield: y})
        return df


chart = Chart()
