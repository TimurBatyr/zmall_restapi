import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send-new_products': {
        'task': 'adds.tasks.send_mail_new_products',
        'schedule': crontab(hour='*/24'),
    },
    'catalog': {
        'task': 'adds.tasks.run_catalog',
        'schedule': crontab(minute=0, hour='1,4,7,10,13,16,19,22'),
    },
    'doska': {
        'task': 'adds.tasks.run_doska',
        'schedule': crontab(minute=0, hour='2,5,8,11,14,17,20,23'),
    },
    'selexy': {
        'task': 'adds.tasks.run_selexy',
        'schedule': crontab(minute=0, hour='0,3,6,9,12,15,18,21'),
    },
}