from django.conf.urls import patterns, url
from nomnom.views import ImportPageView, ExportPageView

urlpatterns = patterns('',
    # TODO: brilliant URL pattern to switch out the template
    # used for the admin change list so that we can
    # overwrite the object tools ONLY
    #
    # URL Patterns Needed
    # /admin/APP_LABEL/MODEL_LABEL/import/, to import data
    # from uploaded files to model;
    # /admin/APP_LABEL/MODEL_LABEL/export/, to export
    # data from a model;
    url(r'^(?P<app_label>\w+)/(?P<model_label>\w+)/import/$',
        ImportPageView.as_view(), name='import'),
    url(r'^(?P<app_label>\w+)/(?P<model_label>\w+)/export/$',
        ExportPageView.as_view(), name='export'),
)
