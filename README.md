# Django Chartflo

Charts for the lazy ones in Django using [Vega Lite](https://vega.github.io/vega-lite).

## Install

Clone and:

`pip install altair django-extensions goerr`

Clone and add to installed apps:

   ```
   "django_extensions",
   "chartflo",
   ```

Migrate the database

## Usage

### Create charts

The charts are created in the code using django-extensions scripts. Make a `scripts` folder in any app. Create a
`make_charts.py` file in this folder and define your charts:

   ```python
   from django.contrib.auth.models import User
   from chartflo.factory import ChartController
   from chartflo.models import Chart
   
   
   def run():
      chart_type = "line"
      x = ("last_login", "last_login:T")
      y = ("username", "count(username):Q")
      width = 870
      height = 180
      users = User.objects.all().order_by("last_login")
      chart = ChartController()
      dataset = chart.serialize_timeseries(
          users, x, y, time_unit="yearmonth", chart_type=chart_type,
          width=width, height=height
      )
      chart, _ = Chart.objects.get_or_create(slug=slug)
      chart.generate(chart, slug, name, dataset)
   ```

For the `x` and `y` axis definitions and the `time_unit` refer to 
the [Altair encoding documentation](https://altair-viz.github.io/documentation/encoding.html)
The generated charts will be saved to the database. 

To generate html files use this setting: `CHARTFLO_TO_HTML = True`. The files will be generated in a `templates/chartflo`
folder.

To run the generator: 

   ```
   python3 manage.py runscript make_charts
   ```

It is also possible to generate individual numbers to include in a widget in the dashboard:

   ```python
   def run():
      num_users = User.objects.all().count()
      num, _ = Number.objects.get_or_create(slug="users")
      num.name = "Users"
      num.legend = "Users"
      num.value = num_users
      num.save()
      num.generate()
   ```

### Compose dashboards

Once we have a few charts it is possible to compose a dashboard in a template by assembling the generated html files, or
from querying the database in a view. The template:

   ```django
{% extends "base.html" %}
{% load staticfiles %}

{% block title %}Users dashboard{% endblock %}

{% block content %}
<link rel="stylesheet" media="screen, projection" href="{% static 'css/chartflo.css' %}" />
{% include "chartflo/head.html" %}
<h1>Users</h1>
	<div>
		{% include "chartflo/numbers/users.html" %}
		{% include "chartflo/numbers/emails.html" %}
		{% include "chartflo/numbers/names.html" %}
		{% include "chartflo/numbers/staff.html" %}
		{% include "chartflo/numbers/superusers.html" %}
	</div>
	<p>
		{% include "chartflo/charts/last_logins.html" %}
	</p>
	<p>
		{% include "chartflo/charts/date_joined.html" %}
	</p>
	<p>
		{% include "chartflo/charts/user_groups.html" %}
	</p>
{% endblock %}
   ```

Make a view and map it to an url:

   ```python
   from django.views.generic import TemplateView


   class UsersDash(TemplateView):
      template_name = "mymodule/dashboards/users.html"
   ```

Check the example folder in the repository for example code: 
[install instructions](https://github.com/synw/django-chartflo/tree/master/example)

### Custom views

Compose views from direct queries

Chart a timeseries query:

   ```python
from chartflo.views import ChartsView
from django.contrib.auth.models import User
from chartflo.factory import ChartController


class ChartView(ChartsView):
    chart_type = "square"
    x = ("last_login", "last_login:T")
    y = ("username", "count(username):Q")
    width = 800
    height = 150
    title = "User last logins"

    def get_data(self):
        users = User.objects.all().order_by("last_login")
        chart = ChartController()
        dataset = chart.serialize_timeseries(
            users, self.x, self.y, time_unit="yearmonth", chart_type=self.chart_type,
            width=self.width, height=self.height, color="username", size="username"
        )
        return dataset
   ```

Chart a count queries dataset:

   ```python
from chartflo.views import ChartsView
from django.contrib.auth.models import User
from chartflo.factory import ChartController


class ChartViewCount(ChartsView):
    chart_type = "bar"
    x = ("group", "group")
    y = ("number", "number:Q")
    width = 550
    height = 250
    title = "User classes"

    def get_data(self):
        users = User.objects.all()
        staff = users.filter(is_staff=True)
        superusers = users.filter(is_superuser=True)
        others = users.filter(is_superuser=False, is_staff=False)
        dataset = {"users": others.count(), "staff": staff.count(),
                   "superuser": superusers.count()}
        chart = ChartController()
        datapack = chart.serialize_count(
            dataset, self.x, self.y, chart_type=self.chart_type,
            width=self.width, height=self.height, color="group"
        )
        return datapack
   ```

Available chart types: `bar`, `circle`, `point`, `square`, `line`, `tick`, `area`

For the syntax of the `x` and `y` fields referer to the 
[Altair encoding documentation](https://altair-viz.github.io/documentation/encoding.html)

### Screenshot

![Dashboard screenshot](https://raw.github.com/synw/django-chartflo/master/docs/img/inflation_dash.png)

