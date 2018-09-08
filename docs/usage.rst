Usage
=====

The dashboards use pre-generated html charts loaded as templates. The charts generation is handled by the 
`Dataswim <https://github.com/synw/dataswim>`_ library, but anything that produces html can be used.

A `demo project <https://github.com/synw/django-chartflo-demo>`_ is available for a complete example

Let's make a simple timeseries module with a dashboard as an example.

Create a model
--------------

This step is optional: charts can be produced without a model

Model (uses `Django Pandas <https://github.com/chrisdev/django-pandas>`_):

.. highlight:: python

::

   from django.db import models
   from django.utils.translation import ugettext_lazy as _
   from django_pandas.managers import DataFrameManager


   class Serie(models.Model):
       date = models.DateField(verbose_name=_("Date"))
       value = models.FloatField(verbose_name=_("Value"))
       objects = DataFrameManager()

       class Meta:
           ordering = ("-date",)
           verbose_name = _("Serie")
           verbose_name_plural = _("Series")
           
Create charts
-------------

Charts creation code in ``pipeline.py``, in a notebook or anywhere. Example for a simple timeline:

::

   from dataswim import ds
   from .models import Serie
   
   
   query = Serie.objects.all()
   # convert the Django query to a Pandas dataframe
   ds.df = query.to_dataframe()
   # set what fields to chart
   ds.chart("date", "value")
   # generate the chart
   c = ds.line_()
   # store the chart for later saving
   ds.stack("timeline", c)
   # set the path where to save it
   ds.report_path = "templates/dashboards/timeseries/charts"
   # save the chart as html file
   ds.to_files()
   
This will save a ``templates/dashboards/timeseries/charts/timeline.html`` html chart

Create a dashboard
------------------

Create a dashboard in the admin with the slug ``timeseries``. Create an inline view for the dashboard and
set it active.

Create templates for the dashboard views
----------------------------------------

Create a template in ``templates/dashboards/timeseries/views/myview_slug.html`` with the view slug as filename:

.. highlight:: django

::

   {% include "templates/dashboards/timeseries/charts/timeline.html" %}
   

Go to ``/dashboards/timeseries/`` to see the result

   