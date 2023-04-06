from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

INTERVAL = 10.0
INTERVAL_FRONTEND = 30.0

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.beat_schedule = {
    # 'update-top-performers-table': {
    #     'task': 'updateTopPerformersTable',
    #     'schedule': INTERVAL,
    # },
    # 'update-top-performers-graph': {
    #     'task': 'updateTopPerformersGraph',
    #     'schedule': 120,
    # },
    # 'update-trending-wallets': {
    #     'task': 'updateTrendingWallets',
    #     'schedule': INTERVAL,
    # },
    # 'update-frontend': {
    #     'task': 'updateFrontend',
    #     'schedule': INTERVAL_FRONTEND
    # },
    # 'update-frontend-profile' : {
    #     'task': 'updateFrontendProfile',
    #     'schedule': INTERVAL_FRONTEND
    # }

}
