# Django Chartflo

Charts for the lazy ones in Django using [Amcharts](https://www.amcharts.com). Just make your query, pack the data and 
its ready. 

## Install

Clone and add `'chartflo',` to INSTALLED_APPS

## Usage

### Generic view

   ```python
   from chartflo.views import ChartsView
   from django.contrib.auth.models import User
   
   
   class MyView(ChartsView):
      chart_type = "pyramid"
      
      def get_data(self):
         users = User.objects.all()
         staff = users.filter(is_staff=True)
         superusers = users.filter(is_superuser=True)
         others = users.filter(is_superuser=False, is_staff=False)
         dataset = {"users": others.count(), "staff": staff.count(),
                   "superuser": superusers.count()}
         return dataset
   ```

### Custom view

  ```python
from chartflo.utils import ChartController
from myapp.models import MyModelToChart

def special_check(field_value):
	if somecheck(field_value) is True:
		return True
	return False

class MyChartsView(TemplateView):
    template_name = 'mytemplate.html'

    def get_context_data(self, **kwargs):
        context = super(MyChartsView, self).get_context_data(**kwargs)
        # get the data
        query = MyModelToChart.objects.all()
        # process count
        chart = ChartController()
        dataset = {}
        dataset["all_objects"] = chart.count(query)
        dataset["published_objects"] = chart.count(query.filter(published=True))
        dataset["special_objects"] = chart.count(query, {"fieldname", special_check})
        # package the data
        datapack = chart.package("chart_id", "Data label", dataset)
        context['datapack'] = datapack
        # options
        datapack['legend'] = True
        datapack['export'] = True
        return context
  ```

You must give a query to ``ChartController.count()``. 

It is also possible to pass field names associated to functions to 
make some custom checks: if this function returns `False` the instance will not be counted.

In the template

   ```django
   {% include "chartflo/charts/pie.html" %}
      <div id="{{ datapack.chart_id }}" style="width: 100%; height: 600px; background-color: #FFFFFF;">
   </div>
   ```

Available charts: `pie.html`, `bar.html`, `pyramid.html`, `timeline.html`

