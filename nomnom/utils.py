from django.db.models.loading import get_model
from django.core.exceptions import ValidationError
from nomnom.settings import NOMNOM_DATA_DIR

import os
import csv

import pdb


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
        
        # dict of related model IDs, for validation before we make any commits
        related_ids_to_test = {}

        with open(NOMNOM_DATA_DIR + '/' + file.name, 'rb') as f:
            reader = csv.DictReader(f)
            for row in reader:
                
                # check for m2m fields
                m2m_cols = []
                for f in model_class._meta.get_m2m_with_model():
                                        
                    if not related_ids_to_test.get(f[0].related.parent_model):
                        related_ids_to_test[f[0].related.parent_model] = []
                    
                    if f[0].name in row.keys():
                        m2m_cols.append({
                            'name' : f[0].name,
                            'model' : f[0].related.parent_model,
                            'ids'   : row[f[0].name]
                        })
                        
                        # ad the ids to a list to check right before we commit
                        for id in row[f[0].name].split(','):
                            if id: related_ids_to_test[f[0].related.parent_model].append(id)
                        
                        del row[f[0].name]
                
                try:
                    # TODO: could this be cleaner?
                    if row.get("id"):
                        try:
                            new_item = model_class.objects.get(id=row.get("id"))
                            for k,v in row.iteritems():
                                setattr(new_item, k, v)
                        except model_class.DoesNotExist:
                            new_item = model_class(**row)
                    else:
                        new_item = model_class(**row)
                    new_item.full_clean()
                except (ValidationError, ValueError) as e:
                    # if the model is not clean send ValidationError
                    return e

                items.append((new_item, m2m_cols,))
                
        for k,v in related_ids_to_test.iteritems():
            nonexistent_ids = set([int(id) for id in v]).difference(set([obj.id for obj in k.objects.all()]))
            if nonexistent_ids:
                return "The following IDs do not exist in the model for the '%s' field: %s" % (f[0].name, unicode(list(nonexistent_ids)).strip('[]'))
            
        
        for item in items:
            item[0].save()
            for m2m_field in item[1]:
                for id in m2m_field['ids'].split(','):
                    if id:
                        try:
                            getattr(item[0], m2m_field['name']).add(m2m_field['model'].objects.get(id=int(id)))
                        except m2m_field['model'].DoesNotExist as e:
                            return e
            
        return None
