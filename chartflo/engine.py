import pandas as pd
from goerr import err
from dataswim import DataSwim
from django.db.models.query import QuerySet
from django_pandas.io import read_frame


class ChartFlo(DataSwim):

    def convert_dataset(self, dataset, x=None, y=None):
        """
        Convert the input data to pandas dataframe
        """
        if type(x) == tuple:
            x = x[0]
        if type(y) == tuple:
            y = y[0]
        try:
            x, y = self._check_fields(x, y)
        except Exception as e:
            err.new(e, self.convert_dataset, "Can not find fields", x, y)
            err.throw()
        df = pd.DataFrame()
        try:
            if isinstance(dataset, pd.DataFrame):
                return dataset
            elif isinstance(dataset, QuerySet):
                df = read_frame(dataset)
            elif isinstance(dataset, dict):
                df = self._dict_to_df(dataset, x, y)
            elif isinstance(dataset, list):
                return pd.DataFrame(dataset)
            else:
                err.new(self.convert_dataset,
                        "Data format unknown: "
                        + str(type(dataset)) +
                        " please provide a dictionnary, a Django Queryset or a Pandas DataFrame")
        except Exception as e:
            err.new(e, self.convert_dataset, "Can not convert dataset")
        if err.exists:
            err.throw()
        return df

    def _check_fields(self, x, y):
        """
        Check if X and Y field are set
        """
        if x is None:
            err.new(self._check_fields,
                    "No X field set: please pass one as parameter")
        if y is None:
            err.new(self._check_fields,
                    "No Y field set: please pass one as parameter")
        return x, y

    def _dict_to_df(self, dictobj, xfield, yfield):
        """
        Converts a dictionary to a pandas dataframe
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
