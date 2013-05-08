from django.db.models.loading import get_model
from django.core.exceptions import ValidationError
from nomnom.settings import NOMNOM_DATA_DIR

import os
import csv


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

        with open(NOMNOM_DATA_DIR + '/' + file.name, 'rb') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # TODO: could this be cleaner?
                    if row.get("id"):
                        new_item, created = model_class.objects.get_or_create(id=row.get("id"))
                        if created:
                            # overwrite new_item
                            new_item = model_class(**row)
                        else:
                            for k,v in row.iteritems():
                                setattr(new_item, k, v)
                    else:
                        new_item = model_class(**row)
                    new_item.full_clean()
                except ValidationError as e:
                    # if the model is not clean send ValidationError
                    return e

                items.append(new_item)

        #model_class.objects.bulk_create(models)
        for item in items:
            item.save()
        return None
