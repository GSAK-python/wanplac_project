from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.contrib import rdb
import datetime
from app1.models import DateList, Kayak, BookingDate


@shared_task
def template_change_date():
    # rdb.set_trace()
    days_list = DateList.objects.values_list('date', flat=True)
    current_day = datetime.datetime.now().date()
    for day in days_list:
        if day == current_day:
            day_to_upload = DateList.objects.filter(date__exact=current_day)
            for object in day_to_upload:
                if object.date == current_day:
                    day = current_day + datetime.timedelta(days=3)
                    object.date = day
                    object.save()
                    object.refresh_from_db()
                    return 'DZIEN ZOSTAL ZAKTUALIZOWANY NA {}'.format(day)


@shared_task
def booking_change_date():
    # rdb.set_trace()
    days_list = BookingDate.objects.values_list('booking_date', flat=True)
    current_day = datetime.datetime.now().date()
    for day in days_list:
        if day == current_day:
            app1_next_day = current_day + datetime.timedelta(days=3)
            app1_next_date = BookingDate.objects.create(booking_date=app1_next_day)
            app1_next_date.save()
            app1_next_date.refresh_from_db()
            return 'DODANO NOWY DZIEN {}'.format(app1_next_day)


@shared_task
def return_kayak_store():
    # rdb.set_trace()
    days_list = BookingDate.objects.values_list('booking_date', flat=True)
    current_day = datetime.datetime.now().date()
    kayak_list = Kayak.objects.all()
    for day in days_list:
        if day == current_day:
            for kayak in kayak_list:
                kayak.store = kayak.stock
                kayak.available = True
                kayak.save()
            return 'LICZBA KAJAKOW ZOSTALA UZUPELNIONA'