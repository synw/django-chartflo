from goerr import Err
from ..utils import _write_file


class DataTable(Err):
    """
    A class to handle data tables
    """

    def create(self, slug, dashboard, query=None, df=None, search=True,
               page_length=25):
        if query is None and df is None:
            self.err("Please provide either a query or a dataframe")
            return
        if query is not None:
            df = query.to_dataframe()
        html = self._html(slug, df, search, page_length)
        _write_file(slug, html, "datatable", dashboard)

    def _html(self, slug, df, search, page_length):
        """
        Renders a html datatable from a dataframe
        """
        cols = df.columns.values
        html = '<table id="' + slug + '" class="table table-bordered table-striped '
        html += 'datatable" data-page-length="' + str(page_length) + '">'
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
        if search is True:
            search = "true"
        else:
            search = "false"
        html += """
              'paging'      : true,
              'lengthChange': false,
              'searching'   : """ + search + """,
              'ordering'    : true,
              'info'        : true,
              'autoWidth'   : true
            })
          })
        </script>"""
        return html
