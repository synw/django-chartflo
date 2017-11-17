from goerr import err
from dataswim import ds
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

    def draw(self, x, y, dataset=None, chart_type="line", opts=None, style=None, label=None):
        """
        Returns a chart object
        """
        if dataset is None:
            if ds.df is None:
                err.new(
                    self.draw, "Dataset not found: use load_data or pass it as parameter")
                err.throw()
            dataset = ds.df
        opts, style, label = self._set_opts(opts, style, label)
        ds.engine = self.engine
        ds.df = self._convert_dataset(dataset)
        chart = ds.chart_(x, y, chart_type, opts, style, label)
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

    def _convert_dataset(self, dataset):
        """
        Convert the input data to pandas dataframe
        """
        return dataset

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
