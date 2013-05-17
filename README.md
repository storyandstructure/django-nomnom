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

PyPI version is coming soon :)

After installation add 'nomnom' to your INSTALLED_APPS setting:

	INSTALLED_APPS = (
	    ...
	    'nomnom', # before the admin app
	    'django.contrib.admin',
	    ...
	)
	
Set up the project URLConf like so:

        urlpatterns = patterns('',
            ...
            url(r'^admin/', include('nomnom.urls')), # before admin url patterns
            url(r'^admin/', include(admin.site.urls)),
			...
        )

Settings
--------

NomNom has the following settings available. You can set them in your project `settings.py`. If you don't set them it will assume the default values:

### NOMNOM\_DATA\_DIR
Saved files will be stored on this directory.

**Default:** `settings.MEDIA_ROOT + 'nomnom'`

Configure Export
----------------

    from nomnom.actions import export_as_csv
    class MyAdmin(admin.ModelAdmin):
        actions = [export_as_csv_action()]
