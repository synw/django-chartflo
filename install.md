# Install 

Install an env:

   ```
   virtualenv -p python3 chartflo_dev
   source bin/activate charflo_dev
   ```
   
Install a fresh Django normally with pip

Create a `templates/base.html` with `{% block content %}{% endblock %}` block

Install dependencies:

   ```
   pip install bokeh django-introspection
   ```

Installed apps:

   ```
   "instrospection",
   "chartflo",
   ```

Urls:

   ```
   url(r'^charts/', include('chartflo.urls')),
   ```
  
Load the fixture for the example users query:

   ```
   python3 manage.py loaddata users_chart.json
   ```

Populate the database with users. 

Go in the admin and save the `Users` question. 

See results at `/charts/dashboard/users/`

