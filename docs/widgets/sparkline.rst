Sparklines
==========

.. image:: https://raw.github.com/synw/django-chartflo/master/docs/img/sparklines.png

A sparkline with a limited number of datapoints.

.. highlight:: python

::

   from chartflo.widgets.sparkline import Sparrkline
   
   
   sp = Sparkline()
   html = sp.simple([1,2,2,4,1])