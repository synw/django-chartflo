# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import importlib
from goerr import err, colors
from django.core.management.base import BaseCommand
import chartflo
from ...utils import copytree


class Command(BaseCommand):
    help = "Create a base dashboard for an app"

    def add_arguments(self, parser):
        parser.add_argument('app', type=str)

    def handle(self, *args, **options):
        app = options["app"]
        # check if module exists
        mod = importlib.util.find_spec(app)
        if mod is None:
            err.new("No module named " + app)
            err.throw()
            return
        # get paths
        origin = os.path.dirname(chartflo.__file__) + "/templates/dashboards"
        dest = os.getcwd() + "/" + app + "/templates/dashboards"
        # check directories
        if not os.path.exists(dest):
            print("Creating directories")
            os.makedirs(dest, exist_ok=True)
        # copy
        print("Copying base templates", "=>", dest)
        try:
            copytree(origin, dest)
        except FileExistsError:
            err.new("The directory", app +
                    "/templates/dashboards/base already exists, aborting")
            err.throw()
            return
        print("[" + colors.green("Ok") + "] Dashboard base template is in",
              app + "/templates/dashboards")
