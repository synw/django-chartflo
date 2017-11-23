# -*- coding: utf-8 -*-

from __future__ import print_function
import time
from django.db.models import Q
from django.core.management.base import BaseCommand
from mqueue.models import MEvent
from chartflo.apps import GENERATORS


def get_changes_events(events_q, last_run_q):
    """
    Get the events objects that occured after the last run of this command
    """

    q = events_q.filter(Q(event_class__icontains="created") | Q(
        event_class__icontains="edited") | Q(event_class__icontains="deleted"))
    if last_run_q is not None:
        q = events_q.filter(
            Q(event_class__icontains="created") |
            Q(event_class__icontains="edited") |
            Q(event_class__icontains="deleted"),

        )
        last_run = last_run_q.date_posted
        q = q.filter(date_posted__gte=last_run)
    return q


def get_changed_models(q):
    """
    Process the events and get the model names that changed
    """
    modelnames = []
    for event in q:
        #print(event.name, event.event_class, event.date_posted)
        if event.content_type:
            modelname = event.content_type.model_class().__name__
            if modelname not in modelnames:
                modelnames.append(modelname)
    return modelnames


def get_generators_to_run(modelnames):
    """
    Get the generators that will need to run, examinating the chart objects
    and check is their associated model changed
    """
    # charts
    generators = []
    for chart in Chart.objects.all():
        for mod in chart.modelnames.split(","):
            if mod in modelnames:
                if chart.generator not in generators:
                    generators.append(chart.generator)
    # numbers
    for num in Number.objects.all():
        for mod in num.modelnames.split(","):
            if mod in modelnames:
                if num.generator not in generators:
                    generators.append(num.generator)
    return generators


def update_charts(events_q, generators, quiet):
    """
    Run the generators
    """
    for generator in generators:
        if quiet == 0:
            print('------------------------------')
            print("Executing generator", generator)
            print('------------------------------')

        try:
            gen = GENERATORS[generator]
        except:
            print("Generator", generator, "not found")
        gen(events_q)


def run_events_generator(events_q):
    """
    Run the events generator
    """
    gen = GENERATORS["mqueue"]
    gen(events_q)


def get_last_run_q():
    try:
        last_run = MEvent.objects.filter(
            event_class="charts_builder").latest("date_posted")
    except:
        return None
    return last_run


def get_events_q(last_run_q=None):
    try:
        if last_run_q is None:
            last_run_q = get_last_run_q()
        events_q = MEvent.objects.filter(
            date_posted__gte=last_run_q.date_posted).order_by(
            "-date_posted").exclude(event_class="charts_builder")
    except:
        last_run_q = None
        events_q = MEvent.objects.all()
    return events_q


def run(quiet):
    """
    Run the all process
    """
    if quiet == 0:
        print("Checking events queue for changes...")
    last_run_q = get_last_run_q()
    events_q = get_events_q(last_run_q)
    if events_q.count() > 0:
        run_events_generator(events_q)
    q = get_changes_events(events_q, last_run_q)
    if quiet == 0:
        print(q.count(), "instances have changed")
    modelnames = get_changed_models(q)
    if quiet == 0:
        print("Changed models:", modelnames)
    generators = get_generators_to_run(modelnames)
    if quiet == 0:
        print("Generators to run", generators)
    update_charts(events_q, generators, quiet)
    # record last run
    MEvent.objects.create(
        name="Events charts builder run", event_class="charts_builder")


class Command(BaseCommand):
    """
    Watch for model changes and run the charts generators
    """
    help = "Process the events queue for changes and run the generators accordingly"

    def add_arguments(self, parser):
        parser.add_argument('-s',
                            dest="timer",
                            default=None,
                            help='Waiting time between runs: ex: -s=5. Will run once if not specified.',
                            )
        parser.add_argument('-q',
                            dest="quiet",
                            action='store_true',
                            default=False,
                            help='Quiet mode: ex: -q.',
                            )

    def handle(self, *args, **options):
        quiet = options["quiet"]
        s = options["timer"]
        if quiet == 0:
            gens = ""
            i = 0
            for generator in GENERATORS:
                gens = gens + generator + " "
                i += 1
            print("Found", i, "generators:", gens)
        run(quiet)
        if s is not None:
            timer = int(s) * 60
            while True:
                print("Sleeping...")
                time.sleep(timer)
                run(quiet)
