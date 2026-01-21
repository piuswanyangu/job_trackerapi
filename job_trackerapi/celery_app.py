import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "job_trackerapi.settings")
app = Celery("job_trackerapi")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()