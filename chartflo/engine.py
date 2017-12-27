import pandas as pd
from goerr import err
from dataswim import DataSwim
from django.db.models.query import QuerySet
from django_pandas.io import read_frame


class ChartFlo(DataSwim):

    def __repr__(self):
        """
        String representation of the object
        """
        rows = str(len(self.df.columns))
        return '<Chartflo object - ' + rows + " >"

    def load_data(self, dataset):
        """
        Set the main dataframe with the input data
        """
        try:
            df = self._load_data(dataset)
            self.df = df
        except Exception as e:
            err.new(e, self.load_data, "Can not load dataset")

    def load_data_(self, dataset):
        """
        Returns an instance with the input data
        """
        try:
            df = self._load_data(dataset)
            return self.clone_(df)
        except Exception as e:
            err.new(e, self._load_data, "Can not load dataset")

    def _load_data(self, dataset):
        """
        Convert the input data to pandas dataframe
        """
        df = pd.DataFrame()
        try:
            if isinstance(dataset, pd.DataFrame):
                return dataset
            elif isinstance(dataset, QuerySet):
                df = read_frame(dataset)
            elif isinstance(dataset, dict):
                df = self._dict_to_df(dataset)
            elif isinstance(dataset, list):
                return pd.DataFrame(dataset)
            else:
                err.new(self._load_data,
                        "Data format unknown: "
                        + str(type(dataset)) +
                        " please provide a dictionnary, a Django Queryset or a Pandas DataFrame")
        except Exception as e:
            err.new(e, self._load_data, "Can not convert dataset")
        if err.exists:
            err.throw()
        return df

    def _dict_to_df(self, dictobj):
        """
        Converts a dictionary to a pandas dataframe
        """
        x = []
        y = []
        print("DICT")
        for datapoint in dictobj:
            x.append(datapoint)
            y.append(dictobj[datapoint])
        df = pd.DataFrame(dictobj)
        return df


cf = ChartFlo()
