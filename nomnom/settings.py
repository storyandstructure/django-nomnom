from django.conf import settings

NOMNOM_DATA_DIR = getattr(settings, 'NOMNOM_DATA_DIR', 'nomnom')
