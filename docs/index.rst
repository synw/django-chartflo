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

   "vv",
   "chartflo",
   
Add to settings:

::

   VV_APPS = ["chartflo"]
   
Add to urls: 

.. highlight:: python

::

   url(r'^dashboards/',include('chartflo.urls')),
   
Run the migrations.


.. toctree::
   :maxdepth: 2
   :caption: Overview
   
   overview.rst

.. toctree::
   :maxdepth: 2
   :caption: Usage
   
   usage.rst
   
.. toctree::
   :maxdepth: 2
   :caption: Widgets
   
   widgets/single_number.rst
   widgets/sparkline.rst
   widgets/datatable.rst

