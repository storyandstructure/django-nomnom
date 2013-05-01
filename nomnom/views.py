from django.views.generic import TemplateView, FormView
from nomnom.forms import ImportFileForm
from django.core import urlresolvers
from django.db.models.loading import get_model
from nomnom.utils import handle_uploaded_file


class ImportPageView(FormView):
    template_name = "nomnom/import_data_form.html"
    form_class = ImportFileForm

    def get_success_url(self, **kwargs):
        return urlresolvers.reverse("admin:%s_%s_changelist" % (self.kwargs.get("app_label"), self.kwargs.get("model_name")))

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        #form.send_email()
        isvalid = super(ImportPageView, self).form_valid(form)
        handle_uploaded_file(self.request.FILES['file'], self.kwargs.get("app_label"), self.kwargs.get("model_name"))
        return isvalid

    def get_context_data(self, **kwargs):
        context = super(ImportPageView, self).get_context_data(**kwargs)
        context['app'] = self.kwargs.get("app_label")
        context['model'] = self.kwargs.get("model_name")
        context['model_plural'] = get_model(self.kwargs.get("app_label"), self.kwargs.get("model_name"))._meta.verbose_name_plural
        return context


class ExportPageView(TemplateView):
    template_name = "nomnom/export_data_form.html"
