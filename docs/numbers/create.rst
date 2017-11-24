Single numbers
==============

A widget showing a single number is available to include in a dashboard. Generate it the same way
as charts:

.. highlight:: python

::

   from django.contrib.auth.models import User
   from chartflo.charts import number
   
   
   def run(events):
    users = User.objects.all(active=True).count()
    number.generate("users", "Users", users, verbose=True,
                    generator="mymodule", modelnames="User", dashboard="my_dashboard",
                    icon="user", color="blue")