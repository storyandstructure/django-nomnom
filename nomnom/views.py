from django.views.generic.base import TemplateView
from django.template.response import TemplateResponse


class ImportPageView(TemplateView):
    template_name = "nomnom/import_data_form.html"

    def get_context_data(self, **kwargs):
        context = super(ImportPageView, self).get_context_data(**kwargs)
        context['app'] = self.kwargs.get("app_label")
        context['model'] = self.kwargs.get("model_name")
        return context
    '''
    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, self.get_template_name(),
                                self.get_context_data())

    def get_template_name(self):
        """Returns the name of the template we should render"""
        return "nomnom/import_data_form.html"

    def get_context_data(self):
        """Returns the data passed to the template"""
        return {
            "import": self.objects.all(),
        }
        '''

class ExportPageView(TemplateView):
    template_name = "nomnom/export_data_form.html"
