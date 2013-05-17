from django.db.models.loading import get_model
from django.core.exceptions import ValidationError
from nomnom.settings import NOMNOM_DATA_DIR

import os
import csv

def get_unique_field_names(model):
    """
    Return all of the fields with "unique=True" for the model
    """
    fields = []
    for field in model._meta.fields:
        if field.unique:
            fields.append(field.name)
    return fields

def get_by_id_or_unique(model, value):
    """
    Try looking up the model by ID first. If that fails, 
    iterate over all unique fields and search until you
    get() a match.
    
    Return the item to save to the field, or an error.
    """
    lookup = None
    try:
        lookup = model.objects.get(id=int(value))
    except model.DoesNotExist:
        return lookup
    except ValueError:
        for field in model._meta.fields:
            if field.unique and field.name != 'id':
                try:
                    lookup = model.objects.get(**{field.name : value})
                    break
                except model.DoesNotExist:
                    pass
    return lookup

def instantiate_from_row(model_class, row):
    """
    Accept a model class and row from a CSV.
    
    Return an unsaved instance of a model based on the row.
    """
    if row.get("id"):
        try:
            new_item = model_class.objects.get(id=row.get("id"))
            del row['id']
        except model_class.DoesNotExist:
            new_item = model_class()
    else:
        new_item = model_class()
        # check if there is a unique field provided, and look up by it
        provided_uniques = set([k for k in row.iterkeys()]) & set(get_unique_field_names(model_class))
        for field_name in provided_uniques:
            try:
                new_item = model_class.objects.get(**{field_name : row[field_name]})
                break
            except model_class.DoesNotExist:
                continue
        
    for field in model_class._meta.fields:
        if row.get(field.name):
            setattr(new_item, field.name, row[field.name])
            
    new_item.full_clean()
    
    return new_item


# http://docs.python.org/2/library/csv.html#csv-examples
def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.DictReader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield dict([(key, unicode(cell, 'utf8')) for key, cell in row.iteritems()])


def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.decode('latin-1').encode('utf-8')


def handle_uploaded_file(file, app_label, model_name):
    items = []
    if not os.path.exists(NOMNOM_DATA_DIR):
        os.makedirs(NOMNOM_DATA_DIR)
    model_class = get_model(app_label, model_name)

    if file:
        destination = open(NOMNOM_DATA_DIR + '/' + file.name, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        
        # dict of related model values, for validation before we make any commits
        related_values_to_test = {}

        with open(NOMNOM_DATA_DIR + '/' + file.name, 'rb') as f:
            reader = unicode_csv_reader(f)
            for row in reader:
                
                # check for m2m fields
                m2m_cols = []
                for f in model_class._meta.get_m2m_with_model():

                    # for now, ignore anything that's not an m2m (or FK)
                    try:
                        related = f[0].related
                    except AttributeError:
                        del row[f[0].name]
                        continue
                                        
                    if not related_values_to_test.get(f[0].related.parent_model):
                        related_values_to_test[f[0].related.parent_model] = []
                    
                    if f[0].name in row.keys():
                        m2m_cols.append({
                            'name' : f[0].name,
                            'model' : f[0].related.parent_model,
                            'values'   : row[f[0].name]
                        })
                        
                        # add the values to a list to check right before we commit
                        for val in row[f[0].name].split(','):
                            if val: related_values_to_test[f[0].related.parent_model].append(val)
                        
                        del row[f[0].name]
                        
                # check for FKs
                for k,v in row.iteritems():
                    if not v:
                        continue
                    fk_lookup = None
                    try:
                        related_field = type(getattr(model_class, k)) # this must be a FK, as the M2M's were removed in the previous step
                        # TODO: how to we catch other types of lookup fields? getattr(model_class, k).field gives us the field type, FYI
                        fk_lookup = model_class._meta.get_field(k).rel.to.objects.get(id=v)
                        row[k] = fk_lookup
                    except ValueError:
                        fk_model = model_class._meta.get_field(k).rel.to
                        for field in fk_model._meta.fields:
                            if field.unique and field.name != 'id':
                                try:
                                    fk_lookup = fk_model.objects.get(**{field.name : v})
                                    row[k] = fk_lookup
                                    break
                                except fk_model.DoesNotExist:
                                    pass
                        
                        if not fk_lookup:
                            return "%s did not return a valid %s." % (v, fk_model._meta.verbose_name)
                        
                    except AttributeError:
                        pass
                            
                try:
                    new_item = instantiate_from_row(model_class, row)
                except (ValidationError, ValueError) as e:
                    # if the model is not clean send ValidationError
                    return e

                items.append((new_item, m2m_cols,))
                
        for k,v in related_values_to_test.iteritems():
            ids_to_check = []
            nonexistent_values = []
            for item in v:
                obj_to_check = get_by_id_or_unique(k,item)
                if not obj_to_check:
                    nonexistent_values.append(item)
            # TODO: the following line efficiently checked for the existence of IDs supplied by the CSV. Now
            # that we're allowing unique field values as lookups as well, we need to rethink this. Perhaps
            # if we know the field we're looking up on we can do the same thing for it?
            #nonexistent_values = set([int(id) for id in v]).difference(set([obj.id for obj in k.objects.all()]))
            if nonexistent_values:
                err_str = ''
                for val in [str(value) for value in nonexistent_values]:
                    err_str += val + ", "
                return "The following values do not exist in the model for the '%s' field: %s" % (f[0].name, err_str)
            
        
        for item in items:
            item[0].save()
            for m2m_field in item[1]:
                for val in m2m_field['values'].split(','):
                    if val:
                        try:
                            getattr(item[0], m2m_field['name']).add(m2m_field['model'].objects.get(id=int(val)))
                        except ValueError:
                            fk_model = m2m_field['model']
                            for field in fk_model._meta.fields:
                                if field.unique and field.name != 'id':
                                    try:
                                        fk_lookup = fk_model.objects.get(**{field.name : val})
                                        getattr(item[0], m2m_field['name']).add(fk_lookup)
                                        break
                                    except fk_model.DoesNotExist:
                                        pass
                            
                            if not fk_lookup:
                                return "%s did not return a valid %s." % (val, fk_model._meta.verbose_name)

                        except m2m_field['model'].DoesNotExist as e:
                            return e
            
        return None
