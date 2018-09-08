Single numbers
==============

.. image:: https://raw.github.com/synw/django-chartflo/master/docs/img/single_number.png

A widget showing a single number is available to include in a dashboard. It can optionaly embed a sparkline.

Simple
------

.. highlight:: python

::

   from chartflo.widgets.number import Number
   
   n = Number()
   html = n.simple(3, "Number label", icon="long-arrow-alt-up")
   n.write("number_slug" , "dashboard_slug", html)
   
   
This will save a ``dashboards/dashboard_slug/numbers/number_slug.html`` file to include in a dashboard view. Icon
is a Font-awesome icon name.


With sparkline
--------------

::

   from chartflo.widgets.number import Number
   
   
   n = Number()
   html = n.simple(3, "Number label", spdata=[1,2,1,3})
   n.write("number_slug" , "dashboard_slug", html)
   