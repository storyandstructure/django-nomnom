from django.core.exceptions import ImproperlyConfigured
from django.db.models.loading import get_model

from nomnom.settings import NOMNOM_DATA_DIR

import csv

def singularize(word):
    """Return the singular form of a word
    singularize('rabbits')
        'rabbit'
    singularize('potatoes')
        'potato'
    singularize('leaves')
        'leaf'
    singularize('knives')
        'knife'
    singularize('spies')
        'spy'
    """
    sing_rules = [lambda w: w[-3:] == 'ies' and w[:-3] + 'y',
                  lambda w: w[-4:] == 'ives' and w[:-4] + 'ife',
                  lambda w: w[-3:] == 'ves' and w[:-3] + 'f',
                  lambda w: w[-2:] == 'es' and w[:-2],
                  lambda w: w[-1:] == 's' and w[:-1],
                  lambda w: w,
                  ]
    word = word.strip()
    singleword = [f(word) for f in sing_rules if f(word) is not False][0]
    return singleword

def handle_uploaded_file(file, app_label, model_name_plural):
    if not NOMNOM_DATA_DIR:
        raise ImproperlyConfigured('You need to specify NOMNOM_DATA_DIR in '
                                   'your Django settings file.')

    model_class = get_model(app_label, singularize(model_name_plural))

    if file:
        destination = open(NOMNOM_DATA_DIR + '/' + file.name, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        
        reader = csv.reader(open(NOMNOM_DATA_DIR + '/' + file.name, 'r'))

        for row in reader:
	        if row[0] != 'id':
				new_item = model_class(id=int(row[0]), name=row[1])
				new_item.save()
