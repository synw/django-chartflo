from goerr import err
from django.conf import settings
from ..utils import _write_file


class Number():
    """
    Class to handle individual numbers
    """

    def simple(self, slug, value, legend=None, unit=None,
               dashboard=None, color="green", icon=None, verbose=True):
        """
        Generates a single number widget
        """
        html = self._simple_html(value, legend, unit, icon, color)
        _write_file(slug, html, "number", dashboard)
        if err.exists:
            if settings.DEBUG is True:
                err.trace()
            else:
                err.throw()
        if verbose is True:
            print("[x] Generated number " + slug)

    def _simple_html(self, number, legend=None, unit=None, icon=None, color="green"):
        """
        Generates html for a simple number widget
        """
        if unit is None:
            unit = ""
        ibg = " bg-" + color
        if icon is None:
            icon = '<span class="info-box-icon' + ibg + \
                '"><i class="fa fa-thumbs-o-up"></i></span>'
        else:
            icon = '<span class="info-box-icon' + ibg + \
                '"><i class="fa fa-' + icon + '"></i></span>'
        if unit != "":
            unit = '<span class="unit">&nbsp;' + unit + '</span>'
        wrapper = '<div class="info-box">'
        res = wrapper + icon + '\n<div class="info-box-content">'
        css_class = ""
        if legend is not None:
            res = res + '\n<span class="info-box-text ' + \
                css_class + '">' + legend + '</span>'
        res = res + '\n<span class="info-box-number">' + \
            str(number) + ' ' + unit + '</span>'
        res = res + "</div></div>"
        return res
