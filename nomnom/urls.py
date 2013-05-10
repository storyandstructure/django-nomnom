from django.conf.urls import patterns, url
from nomnom.views import ImportPageView, export_view

urlpatterns = patterns('',
    # TODO: brilliant URL pattern to switch out the template
    # used for the admin change list so that we can
    # overwrite the object tools ONLY
    url(r'(?P<app_label>\w+)/(?P<model_name>\w+)/import/$', ImportPageView.as_view(), name='import_data'),
    url(r'(?P<app_label>\w+)/(?P<model_name>\w+)/export/(?P<export_type>\w+)/$', export_view, name='export_data'),
)
