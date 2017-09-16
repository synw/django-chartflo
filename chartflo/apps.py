from __future__ import unicode_literals
import importlib
from django.apps import AppConfig


GENERATORS = {}


def load_generators(modname):
    try:
        path = modname + ".chartflo"
        mod = importlib.import_module(path)
        generator = getattr(mod, "run")
        return generator
    except ImportError:
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
            res = load_generators(app)
            if res is not None:
                generators[app] = res
        GENERATORS = generators
