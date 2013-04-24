from django.views.generic.base import TemplateView


class ImportPageView(TemplateView):
    template_name = "import_data_form.html"


class ExportPageView(TemplateView):
    template_name = "export_data_form.html"
