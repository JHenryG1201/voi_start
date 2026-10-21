import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "voi_start.settings")

app = Celery("voi_start")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()