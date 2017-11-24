Compose a dashboard
===================

Once we have a few charts it is possible to compose a dashboard in a template by assembling the generated html files, or
from querying the database in a view. 

Create a template
-----------------

Create a ``templates/dashboards/my_dashboard/index.html`` file:

.. highlight:: django

::

   <div class="row">
    <div class="col-xs-12"><h1>Index</h1>
    <div>{% include "dashboards/mqueue/numbers/events.html" %}</div>
    </div>
   </div>
   
Create a ``templates/dashboards/sidebars/my_dashboard.html`` file:

.. highlight:: django

::

   <ul class="sidebar-menu" data-widget="tree">
    <li class="header">Header</li>
    <li class="treeview">
     <a href="#" onclick="loadDashboard('dashboard_page_name', 'dashboard_name')">Link 1</a>
    </li>
    <li class="treeview">
     <a href="#" onclick="loadDashboard('dashboard_page_name', 'dashboard_name')">Link 2</a>
    </li>
  </ul>

Dashboard view
--------------

To use the generic dashboard view: in url.py:

.. highlight:: python

::

    url(r'^dashboards/', include('chartflo.urls')),


Go to ``/dashboards/my_dashboard/`` where ``my_dashboard`` is the slug of your dashboard

