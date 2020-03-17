from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.contrib import rdb
import datetime
from client_panel.models import Kayak, DateList


@shared_task
def change_date():
    days_list = DateList.objects.values_list('date', flat=True)
    current_time = datetime.datetime.now().time()
    current_day = datetime.datetime.now().date()
    t1 = datetime.time(19, 20)
    for day in days_list:
        if day == current_day and current_time > t1:
            day_to_upload = DateList.objects.filter(date__exact=current_day)
            for object in day_to_upload:
                day = current_day + datetime.timedelta(days=2)
                object.date = day
                object.save()
            return 'Dzien zostal zaktualizowany'


@shared_task
def return_kayak_store():
    # rdb.set_trace()
    days_list = DateList.objects.values_list('date', flat=True)
    kayak_list = Kayak.objects.all()
    current_time = datetime.datetime.now().time()
    current_day = datetime.datetime.now().date()
    return_time = datetime.time(19, 20)
    for day in days_list:
        if day == current_day and current_time >= return_time:
            for kayak in kayak_list:
                kayak.store = kayak.stock
                kayak.save()
            return 'Liczna kajakow zostala uzupelniona'


"""
celery -A wanplac_project  worker --loglevel=info -P solo

celery -A wanplac_project beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

"""