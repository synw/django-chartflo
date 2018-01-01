Sequences
=========

.. image:: https://raw.github.com/synw/django-chartflo/master/docs/img/sequence.png

A widget showing a serie of key/value pairs with optional thresholds.

Example code:

.. highlight:: python

::
   
   from chartflo.apps import cf
   
   
   cf.sequence(widget_slug, "dashboard_name", "Key column", "Value column",
                    style="width:46px;padding:0.2em 0.6em 0.6em 0.2em",
                    trs=dict(high=3.0, low=0))
