from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.contrib import rdb
import datetime
from app2.models import DateList, Kayak


@shared_task
def change_date():
    # rdb.set_trace()
    days_list = DateList.objects.values_list('date', flat=True)
    current_day = datetime.datetime.now().date()
    for day in days_list:
        if day == current_day:
            day_to_upload = DateList.objects.filter(date__exact=current_day)
            for object in day_to_upload:
                day = current_day + datetime.timedelta(days=2)
                object.date = day
                object.save()
            return 'DZIEN ZOSTAL ZAKTUALIZOWANY NA {}'.format(day)


@shared_task
def return_kayak_store():
    # rdb.set_trace()
    days_list = DateList.objects.values_list('date', flat=True)
    current_day = datetime.datetime.now().date()
    kayak_list = Kayak.objects.all()
    for day in days_list:
        if day == current_day:
            for kayak in kayak_list:
                kayak.store = kayak.stock
                kayak.save()
            return 'LICZBA KAJAKOW ZOSTALA UZUPELNIONA'


@shared_task
def get_current_time():
    return datetime.datetime.now().time()


# @shared_task
# def get_current_data():
#     # rdb.set_trace()
#     date_list = DateList.objects.values_list('date', flat=True)
#     next_day = datetime.datetime.now().date() + datetime.timedelta(days=1)
#     next_next_day = datetime.datetime.now().date() + datetime.timedelta(days=2)
#     if current_day in date_list and current_time < change_time:
#         day = current_day
#         return day
#     elif current_day in date_list and current_time >= change_time:
#         day = next_next_day
#         return day
#     elif current_day not in date_list:
#         day = next_day
#         return day


"""
celery -A wanplac_project  worker --loglevel=info -P solo

celery -A wanplac_project beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

"""