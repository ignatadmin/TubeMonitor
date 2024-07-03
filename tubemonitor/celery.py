import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tubemonitor.settings')

app = Celery('tubemonitor')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update_toplists_every_10_min': {
        'task': 'analytic.tasks.update_toplists_task',
        'schedule': crontab(minute='*/10')
    },
}