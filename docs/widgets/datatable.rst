Datables
========

.. image:: https://raw.github.com/synw/django-chartflo/master/docs/img/datatables.png

A widget showing tabular data.

::

   from chartflo.widgets.datatable import DataTable
   
   dt = DataTable()
   # from a dataframe
   dt.create("datatable_slug", "dashboard_slug", df=df, search=False)
   # or from a query
   dt.create("datatable_slug", "dashboard_slug", query=some_django_query)
  
 
This will save a ``dashboards/dashboard_slug/datatables/datatable_slug.html`` file to include in a dashboard view.