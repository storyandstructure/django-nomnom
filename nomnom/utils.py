from django.core.exceptions import ImproperlyConfigured
from django.db.models.loading import get_model

from nomnom.settings import NOMNOM_DATA_DIR

import csv


def handle_uploaded_file(file, app_label, model_name):
    if not NOMNOM_DATA_DIR:
        raise ImproperlyConfigured('You need to specify NOMNOM_DATA_DIR in '
                                   'your Django settings file.')
    model_class = get_model(app_label, model_name)

    if file:
        destination = open(NOMNOM_DATA_DIR + '/' + file.name, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()

        with open(NOMNOM_DATA_DIR + '/' + file.name, 'rb') as f:
            reader = csv.DictReader(f)
            for row in reader:
                new_item = model_class(**row)
                new_item.save()
