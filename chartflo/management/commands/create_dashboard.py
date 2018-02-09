# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import importlib
import shutil
from goerr import err, colors
from django.core.management.base import BaseCommand
import chartflo
from chartflo.models import Dashboard
from ...utils import copytree


def config_template(filename, app):
    with open(filename, 'r') as file:
        filedata = file.read()
        filedata = filedata.replace("base", app)
    with open(filename, 'w') as file:
        file.write(filedata)


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
        # rename stuff
        print("Configuring templates")
        src = dest + "/base"
        des = dest + "/" + app
        shutil.move(src, des)
        # fic imports in files
        config_template(des + "/index.html", app)
        # create dashboard object in the database
        print("Creating dashboard object in the database")
        Dashboard.objects.get_or_create(slug=app, title=app)
        # end msg
        print("[" + colors.green("Ok") + "] Dashboard base template is in",
              app + "/templates/dashboards")
