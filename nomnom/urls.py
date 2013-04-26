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
    #url(r'^admin/(?P<app_label>\w+)/(?P<model_name>\w+)/import/$', ImportPageView.as_view(app=app_label, mod=model_name,), name='import_data'),
    url(r'^import/', ImportPageView.as_view(), name='import_data'),
    url(r'^export/', ExportPageView.as_view(), name='export_data'),
    )
