# Django Chartflo

Charts for the lazy ones in Django. Features:

- **Generate charts** in a declarative way using pure python: no javascript to write

- **Compose dashboards** using the pre-generated html charts. Available widgets:
   - Simple number
   - Number with threshold and progress bar
   - Sparklines
   - Datatables

- **Rebuild the dashboards** on fresh data using generators

Check the [documentation](http://django-chartflo.readthedocs.io/en/latest/index.html) for the install and usage
instructions

Powered by the [Dataswim](https://github.com/synw/dataswim) data analytics library

### Supported rendering engines

- [Holoviews](http://holoviews.org/) and [Bokeh](http://bokeh.pydata.org/)
- [Altair](http://altair-viz.github.io/) and [Vega Lite](https://vega.github.io/vega-lite)
- [Chartjs](http://www.chartjs.org/)
- [Seaborn](http://seaborn.pydata.org/)

## Example notebooks

[Example notebooks](https://github.com/synw/django-chartflo-notebooks) are available to show how to build the charts. 
Click on the badge to run them online:

[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/synw/django-chartflo-notebooks/master)

## Demo project

A demo project is available: 
[check it online](https://chartflo.herokuapp.com/dashboards/inflation/) or visit the
[repository](https://github.com/synw/django-chartflo-demo) to install it locally.

### Screenshot

![Dashboard screenshot](https://raw.github.com/synw/django-chartflo/master/docs/img/inflation_dashboard.png)

## Credits

[Admin LTte](https://adminlte.io/) for the dashboard template

