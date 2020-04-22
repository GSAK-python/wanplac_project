from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wanplac_project.settings')

app = Celery('wanplac_project',
             # broker='amqp://localhost//',
             broker='amqp://test:test@localhost//',
             backend='amqp'
             )
app.conf.broker_heartbeat = 0
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(
    result_expires=3600,
    enable_utc=True,
    timezone='Europe/Warsaw'
)
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'TEMPLATE date change - CLIENT_PANEL': {
        'task': 'client_panel.tasks.template_change_date',
        'schedule': crontab(minute=30, hour=12),
        'args': (),
    },
    'Equalization of store - CLIENT_PANEL': {
        'task': 'client_panel.tasks.return_kayak_store',
        'schedule': crontab(minute=5, hour=12),
        'args': (),
    },
    'BOOKING date change - CLIENT_PANEL': {
        'task': 'client_panel.tasks.booking_change_date',
        'schedule': crontab(minute=10, hour=12),
        'args': (),
    },
    'TEMPLATE date change - APP2': {
        'task': 'app2.tasks.template_change_date',
        'schedule': crontab(minute=30, hour=12),
        'args': (),
    },
    'Equalization of store - APP2': {
        'task': 'app2.tasks.return_kayak_store',
        'schedule': crontab(minute=5, hour=12),
        'args': (),
    },
    'BOOKING date change - APP2': {
        'task': 'app2.tasks.booking_change_date',
        'schedule': crontab(minute=10, hour=12),
        'args': (),
    },
    'TEMPLATE date change - APP1': {
        'task': 'app1.tasks.template_change_date',
        'schedule': crontab(minute=30, hour=12),
        'args': (),
    },
    'Equalization of store - APP1': {
        'task': 'app1.tasks.return_kayak_store',
        'schedule': crontab(minute=5, hour=12),
        'args': (),
    },
    'BOOKING date change - APP1': {
        'task': 'app1.tasks.booking_change_date',
        'schedule': crontab(minute=10, hour=12),
        'args': (),
    }
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))