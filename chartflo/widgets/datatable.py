from goerr import err
from dataswim import ds
from ..utils import _write_file


class DataTable():
    """
    A class to handle data tables
    """

    def create(self, slug, df=None, dashboard=None):
        if df is None:
            if ds.df is None:
                err.new(
                    self.new, "No dataframe set: please provide one in parameter")
                err.throw()
            else:
                df = ds.df
        html = self._html(slug, df)
        _write_file(slug, html, "datatable", dashboard)

    def _html(self, slug, df):
        """
        Renders a html datatable from a dataframe
        """
        cols = df.columns.values
        html = '<table id="' + slug + '" class="table table-bordered table-striped">'
        html += '<thead><tr>'
        for col in cols:
            html += '<th>' + col + '</th>'
        html += '</tr></thead><tbody>'
        for _, row in df.iterrows():
            html += '<tr>'
            for col in cols:
                html += '<td>' + str(row[col]) + '</td>'
            html += '</tr>'
        html += '</tbody></table>'
        return html
