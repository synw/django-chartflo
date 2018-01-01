.. Django Chartflo documentation master file, created by
   sphinx-quickstart on Mon Sep 25 12:26:00 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Django Chartflo
===============

To install: ``pip install django-chartflo``

Add to INSTALLED_APPS: 

.. highlight:: python

::

   "chartflo",
   
Add to urls: 

.. highlight:: python

::

   url(r'^dashboards/',include('chartflo.urls')),
   
Run the migrations.


.. toctree::
   :maxdepth: 2
   :caption: Charts
   
   charts/charts.rst
   
.. toctree::
   :maxdepth: 2
   :caption: Widgets
   
   widgets/single_number.rst
   widgets/number.rst
   widgets/sparkline.rst
   widgets/datatable.rst
   widgets/sequence.rst
   
.. toctree::
   :maxdepth: 2
   :caption: Dashboards
   
   dashboards/compose.rst
   
.. toctree::
   :maxdepth: 2
   :caption: Generators
   
   generators/create.rst
   
.. toctree::
   :maxdepth: 2
   :caption: Charts regeneration
   
   data_change/handle.rst

