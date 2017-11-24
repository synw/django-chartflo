# Django Chartflo

Charts for the lazy ones in Django. Features:

- Generate charts using pure python: no javascript to write
- Compose dashboards using the pre-generated charts

Check the [documentation](http://django-chartflo.readthedocs.io/en/latest/index.html) for the install and usage
instructions

## Supported rendering engines

- [Holoviews](http://holoviews.org/) and [Bokeh](http://bokeh.pydata.org/)
- [Altair](http://altair-viz.github.io/) and [Vega Lite](https://vega.github.io/vega-lite)

## Examples

Example Jupyter notebooks are available. Clone, copy the notebooks in a Django instance, install 
[django-extensions](https://django-extensions.readthedocs.io/en/latest/index.html) and run:

   ```
   python3 manage.py shell_plus --notebook
   ```

## Screenshot

![Dashboard screenshot](https://raw.github.com/synw/django-chartflo/master/docs/img/inflation_dash.png)

