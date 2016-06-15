Django Chartflo
===============

Charts for the lazy ones in Django (using Amcharts). just make your query, pack the data and include a template. 
There is no particular concept to understand nor complicated code to write.

Install
--------------

Clone and add `'chartflo',` to INSTALLED_APPS

Usage
--------------

  ```python
from myapp.models import MyModelToChart

class MyChartsView(TemplateView):
    template_name = 'mytemplate.html'

    def get_context_data(self, **kwargs):
        context = super(MyChartsView, self).get_context_data(**kwargs)
        # get the data
        query = MyModelToChart.objects.all()
        # format the data
        dataset = {}
        for elem in query:
        	if elem.name in dataset.keys():
        		dataset[elem.name] = dataset[elem.name]+1
        else:
        	dataset[elem.name] = 1
        # pack the data
        datapack = {
        		# required
        		'chart_id': 'chart_mymodeltochart',
        		'data_label': 'My model to chart', 
        		'dataset': dataset, 
        		# optional
        		'legend':True
        		}
        context['datapack'] = datapack
        return context
  ```
In the template

   ```django
{% include "chartflo/charts/pie.html" %}
<div id="{{ datapack.chart_id }}" style="width: 100%; height: 600px; background-color: #FFFFFF;">
</div>
   ```
Available charts: `pie.html`, `bar.html`, `pyramid.html`, `timeline.html`

