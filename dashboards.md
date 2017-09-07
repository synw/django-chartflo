# Dashboards

There are two ways to compose dashboards: using the query constructor or using generators. 

## Query constructor

Models details:

### Queries

To create a dashboard start creating queries: fields:

`name`: string, the title

`app`: app name: ex: `auth`

`model`: model name: ex: `User`

`filters`: line string: ex: `is_superuser=False&is_staff=False` to get only the registered users.
Uses the Django filter syntax: `username__icontains=something` is valid.

### Questions

Once you have one or several queries create a question:

`name`: string, the title

`x_field`: name of the x axis field: ex: `last_login`

`x_field_type`: type of the field: ex: `last_login:T`. Refer to the 
[Altair encoding documentation](https://altair-viz.github.io/documentation/encoding.html) for the syntax.

`y_field`: same a x field: ex: `username`

`y_field_type`: same a x field: ex: `count(username):Q`

`chart_type`: select one type

`width`: the chart width

`height`: the chart height

`color`: name of the field to colorize. Adds a legend. Check the Altair encoding doc for details. Ex: `username`

`size`: name of the field to size points from. Check the Altair encoding doc for details. Ex: `username`

`time_unit`: the Altair time unit to use: refer to [the doc](https://altair-viz.github.io/API.html#encoding-channels) for 
the formats. Ex: `yearmonthdate`

`queries`: query or queries associated with the question

`html`: the resulting html

`json`: the resulting Vega Lite json


An example is available with the `dashboard.json` fixture at the root of the repository. This example uses the 
standard `User` model from auth:

   ```
   python3 manage.py loaddata dashboard.json
   ```

Go to the `Test dashboard` object in the admin, unassociate charts and associate questions. Change your data and
save the question again: the charts will be regenerated

Go to `/charts/dashboards/users/`

### Dashboards

When you have several questions then you can create a dashboard:

`title`: the dashboard's title

`slug`: the dashboard's slug

`questions`: the questions attached to the dashboard

`charts`: the charts associated with the dashboard (see below for details about this model)

## Generators

Create scripts to generate `Chart` objects. Model:

`name`: the chart's title

`slug`: the chart's slug

`html`: the resulting html

`json`: the resulting Vega Lite json

This method of generating charts uses the 
[django-extensions script mechanism](https://django-extensions.readthedocs.io/en/latest/runscript.html). 

To see an example copy the `generator_example/scripts` folder into any app, restart the dev server
and run with a management command:

   ```
   python3 manage.py make_charts
   ``` 

This example generates the same charts as the question example. These can be associated to a dashboard.
