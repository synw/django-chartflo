from __future__ import unicode_literals
import importlib
from goerr import err
from django.apps import AppConfig


GENERATORS = {}


def load_generators(modname):
    try:
        path = modname + ".chartflo"
        mod = importlib.import_module(path)
        generator = getattr(mod, "run")
        return generator
    except ImportError as e:
        if "No module named" not in str(e):
            err.new(e)
        return None


class ChartfloConfig(AppConfig):
    name = 'chartflo'
    verbose_name = "Chartflo"

    def ready(self):
        global GENERATORS
        from django.conf import settings
        apps = settings.INSTALLED_APPS
        generators = {}
        for app in apps:
            try:
                res = load_generators(app)
                if res is not None:
                    generators[app] = res
            except Exception as e:
                err.new(e)
        GENERATORS = generators
        if err.exists:
            err.trace()
