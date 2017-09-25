Compose a dashboard
===================

Once we have a few charts it is possible to compose a dashboard in a template by assembling the generated html files, or
from querying the database in a view. 

Create a template
-----------------

.. highlight:: django

::

	{% extends "base.html" %}
	{% load staticfiles %}
	
	{% block title %}Users dashboard{% endblock %}
	
	{% block content %}
	<link rel="stylesheet" media="screen, projection" 
	href="{% static 'css/chartflo.css' %}" />
	{% include "chartflo/head.html" %}
	<h1>Users</h1>
	<div>
	    {% include "chartflo/numbers/users.html" %}
	    {% include "chartflo/numbers/emails.html" %}
	    {% include "chartflo/numbers/names.html" %}
	    {% include "chartflo/numbers/staff.html" %}
	    {% include "chartflo/numbers/superusers.html" %}
	</div>
	<p>
	    {% include "chartflo/charts/last_logins.html" %}
	</p>
	<p>
	    {% include "chartflo/charts/date_joined.html" %}
	</p>
	<p>
	    {% include "chartflo/charts/user_groups.html" %}
	</p>
	{% endblock %}

Dashboard view
--------------

To use the generic dashboard view: in url.py:

.. highlight:: python

::

    url(r'^dashboards/', include('chartflo.urls')),


Go to ``/dashboards/users/`` where ``users`` is the slug of your dashboard, corresponding to the ``generator`` 
parameter supplied to the constructor method.

Example dashboards
------------------

Check django-chartmodels's 
`dashboard <https://github.com/synw/django-chartmodels/blob/master/chartmodels/templates/chartmodels/dashboards/users.html>`_ 
and `generators <https://github.com/synw/django-chartmodels/blob/master/chartmodels/chartflo/users.py>`_ for a full example
