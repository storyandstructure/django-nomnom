import csv
from django.http import HttpResponse

def export_as_csv(modeladmin, request, queryset, export_type):
    """
    Generic csv export admin action.
    based on http://djangosnippets.org/snippets/1697/
    """
    opts = modeladmin._meta
    field_names = set([field.name for field in opts.fields])
    fields = opts.fields
    if fields:
        fieldset = set(fields)
        
    m2m_field_names = set([field_tuple[0].name for field_tuple in opts.get_m2m_with_model()])
    m2m_fields = set([field_tuple[0] for field_tuple in opts.get_m2m_with_model()])
    if m2m_fields:
        m2m_fieldset = set(m2m_fields)

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')

    writer = csv.writer(response)
    #if header:
    if export_type == 'T':
        writer.writerow(list(field_names) + list(m2m_field_names))
    elif export_type == 'D':
        writer.writerow(list(field_names) + list(m2m_field_names))
        for obj in queryset:
            
            m2m_field_output = []
            # I'm not smart enough to do list comprehensions
            for m2m_queryset in [getattr(obj, field).all() for field in m2m_field_names]:
                m2m_field_ids = ""
                for m2m_obj in m2m_queryset:
                    m2m_field_ids += "%s," % m2m_obj.id
                m2m_field_output.append(m2m_field_ids)
            
            other_field_output = []
            for field in field_names:
                try:
                    # this is a ForeignKey field
                    other_field_output.append(getattr(obj, field).id)
                except AttributeError:
                    other_field_output.append(unicode(getattr(obj, field)).encode("utf-8", "replace"))
            
            writer.writerow(other_field_output + m2m_field_output)
    return response


def export_as_csv_action(description="Export selected objects as CSV file",
                         fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        field_names = set([field.name for field in opts.fields])
        if fields:
            fieldset = set(fields)
            field_names = field_names & fieldset
        elif exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')

        writer = csv.writer(response)
        if header:
            writer.writerow(list(field_names))
        for obj in queryset:
            writer.writerow([unicode(getattr(obj, field)).encode("utf-8", "replace") for field in field_names])
        return response
    export_as_csv.short_description = description
    return export_as_csv
