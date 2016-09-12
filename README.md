Django Chartflo
===============

Charts for the lazy ones in Django using [Amcharts](https://www.amcharts.com). Just make your query, pack the data and 
include a template. 
There is no particular concept to understand nor complicated code to write.

Install
--------------

Clone and add `'chartflo',` to INSTALLED_APPS

Usage
--------------

  ```python
from chartflo.utils import ChartDataPack
from myapp.models import MyModelToChart

def special_check(value):
	if somecheck(value) is True:
		return True
	return False

class MyChartsView(TemplateView):
    template_name = 'mytemplate.html'

    def get_context_data(self, **kwargs):
        context = super(MyChartsView, self).get_context_data(**kwargs)
        # get the data
        query = MyModelToChart.objects.all().order_by('name')
		# process count
        P = ChartDataPack()
        dataset = {}
        dataset["all_objects"] = P.count(query)
        dataset["published_objects"] = P.count(query.filter(published=True))
        dataset["special_objects"] = P.count(query, {"fieldname", special_check})
        # package the data
        datapack = P.package("chart_id", "Data label", dataset)
        # options
        datapack['legend'] = True
        datapack['export'] = True
        context['datapack'] = datapack
        return context
  ```

You must give a query to ``ChartDataPack.count``. It is also possible to pass field names associated to functions to 
make some custom checks: if this function returns False the instance will not be counted.

In the template

   ```django
{% include "chartflo/charts/pie.html" %}
<div id="{{ datapack.chart_id }}" style="width: 100%; height: 600px; background-color: #FFFFFF;">
</div>
   ```

Available charts: `pie.html`, `bar.html`, `pyramid.html`, `timeline.html`

