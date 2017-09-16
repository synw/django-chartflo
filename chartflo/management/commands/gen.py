# -*- coding: utf-8 -*-

from __future__ import print_function
from django.core.management.base import BaseCommand
from chartflo.apps import GENERATORS


class Command(BaseCommand):
    help = ""

    def add_arguments(self, parser):
        parser.add_argument('app', type=str)
        parser.add_argument('-q',
                            dest="quiet",
                            default=0,
                            help='Quiet mode: ex: -q=1.',
                            )

    def handle(self, *args, **options):
        """
        Run a generator
        """
        app = options["app"]
        quiet = options["quiet"]
        try:
            generator = GENERATORS[app]
        except:
            if quiet > 0:
                print("Generator not found")
            return
        if quiet > 0:
            print("Running generator", app)
        generator()
