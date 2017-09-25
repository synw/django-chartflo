Single numbers
==============

A widget showing a single number is available to include in a widget in the dashboard. Generate it the same way
as charts:

.. highlight:: python

::

   from chartflo.factory import NumberController
   from django.contrib.auth.models import User
   
   
   def run(events):
      num = NumberController()
      val = User.objects.all().count()
      num.generate("users", "Users", val, 
                   modelnames="User", generator="chart_users"
      )