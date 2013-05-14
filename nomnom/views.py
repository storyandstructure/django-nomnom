from django.views.generic import FormView
from nomnom.forms import ImportFileForm
from django.core import urlresolvers
from django.db.models.loading import get_model
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from nomnom.utils import handle_uploaded_file
from nomnom.actions import export_as_csv


@staff_member_required
def export_view(request, app_label, model_name, export_type):
    modelToExport = get_model(app_label, model_name)
    return export_as_csv(modelToExport, request, modelToExport.objects.all(), export_type)


class ImportPageView(FormView):
    template_name = "nomnom/nomnom_form.html"
    form_class = ImportFileForm
    
    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(ImportPageView, self).dispatch(*args, **kwargs)

    def get_success_url(self, **kwargs):
        return urlresolvers.reverse("admin:%s_%s_changelist" % (self.kwargs.get("app_label"), self.kwargs.get("model_name")))

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        #form.send_email()
        isvalid = super(ImportPageView, self).form_valid(form)
        fileup = handle_uploaded_file(self.request.FILES['file'], self.kwargs.get("app_label"), self.kwargs.get("model_name"))
        if fileup:
            messages.error(self.request, 'Dirty Data : ' + str(fileup))
            return HttpResponseRedirect(reverse('import_data', kwargs=self.kwargs))
        return isvalid

    def get_context_data(self, **kwargs):
        context = super(ImportPageView, self).get_context_data(**kwargs)
        context['app'] = self.kwargs.get("app_label")
        context['model'] = self.kwargs.get("model_name")
        context['change_list_url'] = reverse("admin:%s_%s_changelist" % (self.kwargs.get("app_label"), self.kwargs.get("model_name")))
        context['model_plural'] = get_model(self.kwargs.get("app_label"), self.kwargs.get("model_name"))._meta.verbose_name_plural
        return context
