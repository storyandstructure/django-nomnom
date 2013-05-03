django-nomnom
=============

A generic importing tool for the Django admin site.

Developed with
--------------

 * Python 2.7.x
 * Django 1.4.x

Installation & Setup
--------------------
Currently you can install django-nomnom via pip like so:

    pip install -e git+https://github.com/storyandstructure/django-nomnom.git#egg=nomnom

PyPI version coming soon :)

After installation you need configure your project to recognizes the NomNom application adding 'nomnom' to your INSTALLED_APPS setting and setup the project URLConf like follow:

        urlpatterns = patterns('',
            # ...
            url(r'^admin/', include('nomnom.urls')), # put it before admin url patterns
            url(r'^admin/', include(admin.site.urls)),
        )

Settings
--------

NomNom has the following settings available. You can set them in your project settings.py. If you don't set them it will assume the default values:

NOMNOM_DATA_DIR
Saved files will be stored on this directory. Default: None.

Configure Export
----------------
from nomnom.actions import export_as_csv
class MyAdmin(admin.ModelAdmin):
    actions = [export_as_csv_action()]
