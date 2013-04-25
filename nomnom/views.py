from django.views.generic.base import TemplateView


class ImportPageView(TemplateView):
    template_name = "nomnom/import_data_form.html"


class ExportPageView(TemplateView):
    template_name = "nomnom/export_data_form.html"
