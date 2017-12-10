from goerr import err
from ..utils import _write_file
from chartflo.serializers import convert_dataset


class DataTable():
    """
    A class to handle data tables
    """

    def create(self, slug, dataset, dashboard=None):
        df = convert_dataset(dataset)
        if df is None:
            if df is None:
                err.new(
                    self.new, "No dataframe set: please provide one in parameter")
                err.throw()
            else:
                df = df
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
        html += '<script>'
        html += '$(function () {'
        html += '$("#' + slug + '").DataTable({'
        html += """
              'paging'      : true,
              'lengthChange': true,
              'searching'   : true,
              'ordering'    : true,
              'info'        : true,
              'autoWidth'   : true
            })
          })
        </script>"""
        return html
