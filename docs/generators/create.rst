Charts
======

To charts are created using python generators: the user defines the data and the chart options. Html files are 
generated and included in templates to view them.

Define a ``chartflo.py`` file or package in any app with a ``run`` function. This is where the generators live. These
files will be detected at startup and the generators will be registered.

Write a generator
-----------------

Example chart for user groups: in ``myapp/chartflo.py``:

.. highlight:: python

::

   from django.contrib.auth.models import User
   from chartflo.charts import chart
   
   
   def get_data():
    groups = Group.objects.all()
    groups_count = {}
    for group in groups:
     count = group.user_set.count()
     groups_count[group.name] = count
    return groups_count)
   
   
   def run(events):
    groups_count = get_data()
    # get the chart
    c = chart.draw(groups_count, "Name", "Num", "bar")
    # store it for later export
    # params are: slug, title, chart object
    chart.stack("groups", "Groups", c)
    # export the chart to files
    path = "dashboards/my_dashboard/charts"
    chart.export(path)
      
This will create a basic bar charts comparing the number of members in user groups.

Available chart types: `bar`, `circle`, `point`, `square`, `line`, `tick`, `area`, `rule`

Create a ``templates/dashboards/my_dashboard/charts`` directory where the html files to be generated and run the generator

Rendering engines
-----------------

The default rendering engine is Bokeh. To use Altair set it first: ``chart.engine = "altair"``.


Encoding options
----------------

For the ``x`` and ``y`` axis definitions and the ``time_unit`` when using Altair refer to 
the `Altair encoding documentation <https://altair-viz.github.io/documentation/encoding.html>`_

Run the generator
-----------------

Run the generator with a management command to generate the html files: 

.. highlight:: python

::
   
   python3 manage.py gen myapp -all


Subgenerators
-------------

An app can contain multiple subgenerators: to use this feature create a ``chartflo`` package in an app:

::
   
   __init__.py
   mysubgenerator.py
   
The ``__init__.py`` contains the main generator with its ``run`` function. The ``subgenerator.py`` also has to have a
``run`` function. To launch a subgenerator:

.. highlight:: python

::
   
   python3 manage.py gen myapp.mysubgenerator

