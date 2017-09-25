Handle data changes
===================

The charts regeneration on data changes is handled by a worker in a management command.

Install: ``pip install django-mqueue`` and add ``"mqueue",`` to installed apps to get the events queue.

In settings register the models that need to be watched:

.. highlight:: python

::

   MQUEUE_AUTOREGISTER = [
      ('django.contrib.auth.models.User', ["c", "u", "d"]),
   ]

Check the 
`Mqueue documentation <http://django-mqueue.readthedocs.io/en/latest/usage/registered_models.html>`_ for more info 
about the models registration mechanism.

This will produce events on each create, delete and update operation for the ``auth.User`` model. Two options are possible
to handle the changes:

Use a worker to regenerate the charts
-------------------------------------

The worker looks at model changes since his last run and launches the generators. Each chart and number are associated to
some models and a generator. Run the management command:

.. highlight:: bash

::

   python3 manage.py gencharts
   
This will run the command once and exit. To run it at fixed intervals:

``-s=10``: this will run the command every 10 minutes

To run quietly: ``-q``

To run one generator only use: ``python3 manage.py gen myapp``

Regenerate the charts immediately on data change
------------------------------------------------

Process the regeneration immediatly after the event is fired: create a ``generate.py`` file in your module:

.. highlight:: python

::

   from django.core.management import call_command
   from django.contrib.auth.models import User

   def save(event, conf):
    if event.content_type is not None:
        if event.content_type.model_class() == User:
            call_command("gen", "myapp")
   
Where ``"myapp"`` is the name of the app where your generator script is. Then in settings:

.. highlight:: python

::

    MQUEUE_HOOKS = {
       "chartflo": {
         "path": "mymodule.generate",
       }
    }

This way the charts generation command will be executed at each create, delete update action on the model
