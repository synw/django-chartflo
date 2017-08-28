# Install 

You will need conda to get the latest bokeh library (required):

https://www.anaconda.com/distribution/

Install an env:

   ```
   conda create -n chartflo_dev bokeh pip
   source activate charflo_dev
   ```
   
Install a fresh Django normally with pip

Create a `templates/base.html` with `{% block content %}{% endblock %}` block

Install dependency:

   ```
   pip install django-instrospection
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
   
Populate the database with users and go to `/charts/dashboard/users/`

