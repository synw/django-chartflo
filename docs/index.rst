.. Django Chartflo documentation master file, created by
   sphinx-quickstart on Mon Sep 25 12:26:00 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Django Chartflo
===============

To install: clone and ``pip install altair goerr blessings gencharts``

Add to INSTALLED_APPS: 

.. highlight:: python

::

   "chartflo",
   
Run the migrations.

.. toctree::
   :maxdepth: 2
   :caption: Create charts
   
   generators/create.rst
   numbers/create.rst
   
.. toctree::
   :maxdepth: 2
   :caption: Dashboards
   
   dashboards/compose.rst
   
.. toctree::
   :maxdepth: 2
   :caption: Charts regeneration
   
   data_change/handle.rst

