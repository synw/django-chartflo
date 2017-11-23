import pandas as pd
from goerr import err
from dataswim import ds
from django.db.models.query import QuerySet
from django.utils._os import safe_join
from django.conf import settings


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

    def draw(self, dataset=None, x=None, y=None, chart_type="line", opts=None, style=None, label=None):
        """
        Returns a chart object
        """
        if dataset is None:
            if ds.df is None:
                err.new(
                    self.draw, "Dataset not found: use load_data or pass it as parameter")
                err.throw(True)
            dataset = ds.df
        try:
            opts, style, label = self._set_opts(opts, style, label)
            ds.engine = self.engine
            ds.df = self.convert_dataset(dataset, x, y)
            chart = ds.chart_(x, y, chart_type, opts, style, label)
        except Exception as e:
            err.new(e, self.draw, "Can not draw chart")
            err.throw(True)
        return chart

    def stack(self, slug, title, chart_obj=None):
        """
        Save reports to files
        """
        ds.stack(slug, title, chart_obj)

    def export(self, folderpath):
        """
        Save reports to files
        """
        path = safe_join(settings.BASE_DIR, "templates/" + folderpath)
        print("PATH", path)
        ds.to_files(path)

    def load_data(self, title, data, **args):
        """
        Loads data in the pandas dataframe format
        """
        ds.set_df(data, **args)
        ds.index_col(title)

    def check(self):
        """
        Returns a view of the chart's data
        """
        return ds.df.head()

    def convert_dataset(self, dataset, x=None, y=None):
        """
        Convert the input data to pandas dataframe
        """
        try:
            self._check_fields(x, y)
        except Exception as e:
            err.new(e, self.convert_dataset, "Can not find fields", x, y)
            err.throw()
        try:
            if isinstance(dataset, QuerySet):
                x_vals = []
                y_vals = []
                for row in dataset.values():
                    y_vals.append(row[x])
                    x_vals.append(row[y])
                dataset = pd.DataFrame({x: x_vals, y: y_vals})
            elif isinstance(dataset, dict):
                dataset = self._dict_to_df(dataset, x, y)
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
        df = pd.DataFrame({xfield: x, yfield: y})
        return df

    def _set_opts(self, opts, style, label):
        """
        Set the chart options from input or defaults
        """
        if opts is None:
            opts = self.opts
        else:
            self.opts = opts
        if style is None:
            style = self.style
        else:
            self.style = style
        if label is None:
            label = ""
        return opts, style, label


class Number():
    """
    Class to handle individual numbers
    """

    def generate(self, slug, legend, value, generator, unit="",
                 verbose=False, modelnames="", thresholds={}):
        """
        Create or update a number instance from a value
        """
        defaults = {"legend": legend, "value": value, "unit": unit}
        num, created = Number.objects.get_or_create(
            slug=slug, defaults=defaults)
        if created is False:
            num.legend = legend
            num.value = value
            num.unit = unit
            num.generator = generator
            num.modelnames = modelnames
            num.thresholds = thresholds
            num.save()
        num.generate()
        if verbose is True:
            print("[x] Generated number", legend)


chart = Chart()
number = Number()
