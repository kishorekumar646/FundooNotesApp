from __future__ import absolute_import, unicode_literals
from celery import Celery
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from djcelery.models import PeriodicTask
import datetime

app = Celery('tasks', broker='redis://localhost:6379')


@app.task
def reminder():
    print("see you in 10 seconds")
