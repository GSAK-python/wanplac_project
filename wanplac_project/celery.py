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
)
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'Data change every day at EXACT TIME': {
        'task': 'client_panel.tasks.change_date',
        'schedule': crontab(),
        'args': (),
    },
    'Equalization of kayak store to stock ammount': {
        'task': 'client_panel.tasks.return_kayak_store',
        'schedule': crontab(),
        'args': (),
    }
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))