import os
from django.conf import settings

data_dir = "nomnom"
if settings.MEDIA_ROOT:
	data_dir = os.path.join(settings.MEDIA_ROOT, 'nomnom')

NOMNOM_DATA_DIR = getattr(settings, 'NOMNOM_DATA_DIR', data_dir)
