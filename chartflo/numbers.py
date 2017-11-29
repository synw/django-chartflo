from goerr import err
from django.conf import settings
from .utils import _write_file
from .widgets import number as num


class Number():
    """
    Class to handle individual numbers
    """

    def simple(self, slug, value, legend=None, unit=None,
               dashboard=None, color="green", icon=None, verbose=True):
        """
        Generates a single number widget
        """
        html = num(value, legend, unit, icon, color)
        _write_file(slug, html, "number", dashboard)
        if err.exists:
            if settings.DEBUG is True:
                err.trace()
            else:
                err.throw()
        if verbose is True:
            print("[x] Generated number " + slug)


number = Number()
