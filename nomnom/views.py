from django.views.generic.base import TemplateView
from django.template.response import TemplateResponse
#from nomnom.forms import ImportFileForm


class ImportPageView(TemplateView):
    template_name = "nomnom/import_data_form.html"

    def get_context_data(self, **kwargs):
        context = super(ImportPageView, self).get_context_data(**kwargs)
        context['app'] = self.kwargs.get("app_label")
        context['model'] = self.kwargs.get("model_name")
        return context

class ExportPageView(TemplateView):
    template_name = "nomnom/export_data_form.html"
