from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.contrib import rdb
import datetime
from datetime import timedelta
from app2.models import DateList, Kayak, BookingDate, Booking, TermKayaks


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
            app2_next_day = current_day + datetime.timedelta(days=3)
            app2_next_date = BookingDate.objects.create(booking_date=app2_next_day)
            app2_next_date.save()
            app2_next_date.refresh_from_db()
            return 'DODANO NOWY DZIEN {}'.format(app2_next_day)


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


@shared_task
def is_booking_active_this_day():
    # rdb.set_trace()
    booking_list = Booking.objects.all()
    term_kayaks = TermKayaks.objects.all()
    active_booking_after_9 = []
    inactive_booking_after_9 = []
    expired_booking_after_9 = []
    threshold_time = datetime.time(7)
    current_time = datetime.datetime.now().time()
    current_day = datetime.datetime.now().date()
    for booking in booking_list:
        max_booking_confirm_time = booking.exact_time + timedelta(hours=1)
        if booking.exact_time.date() == current_day:
            if booking.exact_time.time() > threshold_time:
                if booking.active is True:
                    active_booking_after_9.append('Rezerwacja {} ACTIVE'.format(booking.code))
                elif booking.active is False and current_time < max_booking_confirm_time.time():
                    inactive_booking_after_9.append('Rezerwacja {} WAITING FOR ACTIVE'.format(booking.code))
                elif booking.active is False and current_time >= max_booking_confirm_time.time():
                    for detail in term_kayaks:
                        if detail.booking.active is False and booking.id == detail.booking_id:
                            detail.kayak.store += detail.quantity
                            detail.kayak.save()
                            expired_booking_after_9.append(
                                'Dodano {} sztuk {} do stanu z zamówienia {}'.format(detail.quantity,
                                                                                     detail.kayak.name,
                                                                                     detail.booking.code))

    return list(dict.fromkeys(active_booking_after_9)), list(
        dict.fromkeys(inactive_booking_after_9)), expired_booking_after_9

"""
celery -A wanplac_project  worker --loglevel=info -P solo

celery -A wanplac_project beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

"""