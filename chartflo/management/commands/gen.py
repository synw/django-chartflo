# -*- coding: utf-8 -*-

from __future__ import print_function
from django.core.management.base import BaseCommand
from django.conf import settings
from chartflo.apps import GENERATORS, load_generator
from goerr import err
from .gencharts import get_changes_events, get_last_run_q, get_events_q
from mqueue.models import MEvent


class Command(BaseCommand):
    help = ""

    def add_arguments(self, parser):
        parser.add_argument('app', type=str)
        parser.add_argument('-q',
                            dest="quiet",
                            action='store_true',
                            default=False,
                            help='Quiet mode: ex: -q',
                            )
        parser.add_argument('-all',
                            action='store_true',
                            dest="all",
                            default=False,
                            help='Update for all instances: ex: -all',
                            )

    def handle(self, *args, **options):
        """
        Run a generator
        """
        app = options["app"]
        quiet = int(options["quiet"])
        runall = int(options["all"])
        subgenerator = None
        if "." in app:
            l = app.split(".")
            app = l[0]
            subgenerator = l[1]
        try:
            generator = GENERATORS[app]
            if subgenerator is not None:
                generator = load_generator(app, subgenerator)
                if generator is None:
                    err.new("Subgenerator " + subgenerator + " not found")
                    err.trace()
                    return
        except Exception as e:
            err.new(e, "Generator not found")
            err.report()
            return
        if quiet > 0:
            print("Running generator", app)
        try:
            last_run_q = get_last_run_q()
        except Exception:
            pass
        if runall == 0:
            try:
                events_q = get_events_q()
            except Exception as e:
                err.new(e)
            try:
                events_q = get_changes_events(events_q, last_run_q)
            except Exception as e:
                err.new(e)
        else:
            try:
                events_q = MEvent.objects.all()
            except Exception as e:
                err.new(e)
        try:
            generator(events_q)
        except Exception as e:
            err.new(e)
        if err.exists:
            if settings.DEBUG is True:
                err.throw()
            else:
                err.report()
