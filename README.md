django-nomnom
=============

A generic importing tool for the Django admin site.

Developed with
--------------

 * Python 2.7.x
 * Django 1.4.x

Settings
--------

NomNom has the following settings available. You can set them in your project settings.py. If you don't set them it will assume the default values:

NOMNOM_DATA_DIR
Saved files will be stored on this directory. Default: None.

urls.py
-------

Nomnom provides specific urls to handle file export and import. Add the following lines to the end of your project's default urls.py:

    from nomnom.urls import urlpatterns as nomnom_urls
		urlpatterns += nomnom_urls

Configure Export
----------------
from nomnom.actions import export_as_csv
class MyAdmin(admin.ModelAdmin):
    actions = [export_as_csv_action()]
