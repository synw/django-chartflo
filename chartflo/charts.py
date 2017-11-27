import pandas as pd
from goerr import err
from dataswim import ds
from django.db.models.query import QuerySet
from django.utils._os import safe_join
from django.conf import settings
from .models import Number as Num


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

    def draw(self, dataset=None, x=None, y=None, chart_type="line",
             opts=None, style=None, label=None, num_col=None, index_col=None):
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
            if num_col is not None:
                self.num_col(num_col[0])
        except Exception as e:
            self.err(e, self.draw, "Can not add numeric column")
        try:
            if index_col is not None:
                self.index_col(index_col)
        except Exception as e:
            self.err(e, self.draw, "Can not add index column")
        try:
            opts, style, label = self._set_opts(opts, style, label)
            ds.engine = self.engine
            ds.df = self.convert_dataset(dataset, x, y)
            chart = ds.chart_(x, y, chart_type, opts, style, label)
            return chart
        except Exception as e:
            err.new(e, self.draw, "Can not draw chart")
            err.throw(True)

    def stack(self, slug, title, chart_obj=None):
        """
        Save reports to files
        """
        try:
            ds.stack(slug, title, chart_obj)
        except Exception as e:
            err.new(e, self.draw, "Can not stack chart")
            err.throw(True)

    def export(self, folderpath):
        """
        Save reports to files
        """
        try:
            path = safe_join(settings.BASE_DIR, "templates/" + folderpath)
            ds.to_files(path)
        except Exception as e:
            err.new(e, self.draw, "Can not export chart to " + path)
            err.throw(True)

    def load_data(self, title, data, **args):
        """
        Loads data in the pandas dataframe format
        """
        try:
            ds.set_df(data, **args)
            ds.index_col(title)
        except Exception as e:
            err.new(e, self.draw, "Can not load data")
            err.throw(True)

    def check(self):
        """
        Returns a view of the chart's data
        """
        return ds.df.head()

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

    def num_col(self, name="num", value=1):
        """
        Add a numeric column to the main dataframe
        """
        ds.add(name, value)

    def index_col(self, col):
        """
        Add an index to the main dataframe
        """
        print(ds.df.columns.values)
        ds.index_col(col)

    def serialize_date(self, date):
        """
        Serialize a data to a proper Altair format
        """
        return date.strftime('%Y-%m-%d %H:%M:%S')

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
                 verbose=False, modelnames="", thresholds={}, dashboard=None, color="green", icon=None, progress=None):
        """
        Create or update a number instance from a value
        """
        defaults = {"legend": legend, "value": value, "unit": unit}
        num, created = Num.objects.get_or_create(
            slug=slug, defaults=defaults)
        if created is False:
            num.legend = legend
            num.value = value
            num.unit = unit
            num.generator = generator
            num.modelnames = modelnames
            num.thresholds = thresholds
            num.save()
        num.generate(dashboard, icon=icon, color=color, progress=progress)
        if verbose is True:
            print("[x] Generated number", legend)


chart = Chart()
number = Number()
