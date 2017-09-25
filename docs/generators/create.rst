Charts
======

To charts are created using python generators: the user defines the data and the chart options. Html files are 
generated and included in templates to view them.

Define a ``chartflo.py`` file or package in any app with a ``run`` function. This is where the generators live. These
files will be detected at startup and the generators will be registered.

Write a generator
-----------------

Example chart for last logins using the auth.User model: in ``myapp/chartflo.py``:

.. highlight:: python

::

   from django.contrib.auth.models import User
   from chartflo.factory import ChartController
   
   
   def run(events):
      chart = ChartController()
      x = ("last_login", "last_login:T")
      y = ("username", "count(username):Q")
      q = User.objects.all().order_by("last_login")
      chart_type = "line"
      width = 870
      height = 180
      slug = "last_logins"
      name = "Last logins"
      time_unit = "yearmonth"
      chart.generate(
          slug, name, chart_type, q, x, y,
          width, height, time_unit=time_unit, verbose=True, 
          modelnames="User", generator="chart_users"
      )
      
This will create a line chart showing the last logins with a timeseries ``x`` axis and a quantitative ``y``
axis. The generated charts will be saved to the database. 

Create a ``templates/chartflo`` directory where the html files will be generated

Encoding options
----------------

For the ``x`` and ``y`` axis definitions and the ``time_unit`` refer to 
the `Altair encoding documentation <https://altair-viz.github.io/documentation/encoding.html>`_

Settings
--------

To generate Vega Lite encoded json files use this setting: ``CHARTFLO_TO_JSON = True``: the files
will be generated in ``templates/chartflo/json/charts``

To not generate html use this use this setting: ``CHARTFLO_TO_HTML = False``

Run the generator
-----------------

Run the generator with a management command to generate the html files: 

   ```
   python3 manage.py gen myapp -all
   ```  