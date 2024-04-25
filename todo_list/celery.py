import os

from celery import Celery
from celery.schedules import crontab
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_list.settings')

app = Celery('todo_list')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
# ========================================================================================
app.conf.beat_schedule = {
# create an object for your scheduling your task
    'fetch-and-store-temp-data-contrab': {
        'task': 'geospatial.geojsonapi.weatherpostapi', #app_name.tasks.function_name
        'schedule': crontab(), #crontab() means run every minute
        # 'args' : (..., ...) In case function takes parameters, add them here
    }
} 