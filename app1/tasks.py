from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.contrib import rdb
import datetime
from app1.models import DateList, Kayak, BookingDate, Booking, TermKayaks


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


@shared_task
def is_booking_active():
    # rdb.set_trace()
    booking_list = Booking.objects.all()
    term_kayaks = TermKayaks.objects.all()
    active_booking = []
    inactive_booking = []
    expired_booking = []
    change_time = datetime.time(14, 57)
    current_time = datetime.datetime.now().time()
    for booking in booking_list:
        if booking.active is True:
            active_booking.append('Rezerwacja {} została potwierdzona'.format(booking.code))
        else:
            if current_time <= change_time:
                inactive_booking.append('Rezerwacja {} nie została jeszcze potwierdzona'.format(booking.code))
            if current_time > change_time:
                for detail in term_kayaks:
                    if detail.booking.active is False and booking.id == detail.booking_id:
                        detail.kayak.store += detail.quantity
                        detail.kayak.save()
                        expired_booking.append('Dodano {} sztuk {} do stanu z zamówienia {}'.format(detail.quantity, detail.kayak.name, detail.booking.code))

    return list(dict.fromkeys(active_booking)), list(dict.fromkeys(inactive_booking)), expired_booking

