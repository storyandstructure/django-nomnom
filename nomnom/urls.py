from django.conf.urls import patterns, url
from nomnom.views import ImportPageView, ExportPageView

urlpatterns = patterns('',
    # TODO: brilliant URL pattern to switch out the template
    # used for the admin change list so that we can
    # overwrite the object tools ONLY
    #
    # APP_LABEL
    # MODEL_LABEL
    url(r'^(?P<app_label>\w+)/(?P<model_name>\w+)/import/$', ImportPageView.as_view(), name='import_data'),
    url(r'^(?P<app_label>\w+)/(?P<model_name>\w+)/export/$', ExportPageView.as_view(), name='export_data'),
)
