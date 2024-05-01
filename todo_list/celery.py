import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_list.settings')

app = Celery('todo_list')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

app.conf.beat_schedule = {
    'fetch-and-store-temp-data-contrab': {
        'task': 'geospatial.geojsonapi.weatherpostapi', 
        'schedule': crontab(minute=0, hour=0),

      
    }
} 