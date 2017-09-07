# Django Chartflo

Charts for the lazy ones in Django using [Vega Lite](https://vega.github.io/vega-lite). 
Just make your query, pack the data and its ready. 

## Install

`pip install altair django-extensions django-introspection`

Clone and add to INSTALLED_APPS:

   ```
   "django_extensions",
   "introspection",
   "chartflo",
   ```
   
Add to urls:

   ```
   url(r'^charts/', include('chartflo.urls')),
   ```

Make the migrations

## Dashboards

Check the [dashboard doc](dashboards.md)

## Views

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

Available chart types: `bar`, `circle`, `point`, `square`, `line`, `tick`

For the syntax of the `x` and `y` fields referer to the 
[Altair encoding documentation](https://altair-viz.github.io/documentation/encoding.html)
