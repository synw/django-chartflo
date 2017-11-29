from goerr import err
from django.conf import settings
from ..utils import _write_file


class Sparkline():
    """
    Class to handle sparklines
    """

    def simple(self, slug, data, dashboard=None, verbose=True):
        """
        Generates a single sparkline
        """
        html = self._simple_html(data)
        _write_file(slug, html, "sparkline", dashboard)
        if err.exists:
            if settings.DEBUG is True:
                err.trace()
            else:
                err.throw()
        if verbose is True:
            print("[x] Generated sparkline " + slug)

    def _simple_html(self, data):
        w = """<span class="sparkline sparkline-inline" data-type="line" 
           data-spot-Radius="3" data-highlight-Spot-Color="#f39c12" data-highlight-Line-Color="#222" 
           data-min-Spot-Color="#f56954" data-max-Spot-Color="#00a65a" data-spot-Color="#39CCCC" 
           data-offset="90" data-width="50px" data-height="15px" data-line-Width="2" 
           data-line-Color="#39CCCC" data-fill-Color="rgba(57, 204, 204, 0.08)">"""
        strdata = [str(x) for x in data]
        w += ",".join(strdata)
        w += "</span>"
        return w
