## Install

Get the dependencies: `pip install altair django-extensions goerr blessings django-seed`

Create a Django instance. Copy the `scripts` folder and the `views.py` file in any app.

Map an url to the view:

   ```python
   from myapp.views import UsersDash
   
   urlpatterns = [
      # ...
      url(r'^dashboards/users/$', UsersDash.as_view()),
   ]
   ```
   
Clone and add to installed apps:

   ```
   "django_extensions",
   "chartflo",
   "django_seed",
   ```

Migrate the database

Add the setting `CHARTFLO_TO_HTML = True`

## Run

Populate the database with fake data: `python3 manage.py seed auth --number=100`

Create a `/templates` folder and copy `base.html` in it. Create a `/templates/dashboards/` folder and
copy `users.html` in it.

Run the generator: `python3 manage.py runscript chart_users`. Html files will be generated in `templates/charflo`

Go to `/dashboards/users/` to see the results

![Users dashboard screenshot](https://raw.github.com/synw/django-chartflo/master/docs/img/users_dash.png)

