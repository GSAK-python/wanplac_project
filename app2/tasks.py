from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.contrib import rdb
import datetime
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
def is_booking_active_before_day():
    """
    For booking that where made atleast day before today or same day to 7 a.m
    booking has to be confirmed till 9 a.m.
    :return: - return 3 lists - first with active booking, second with booking waiting for activations, third with faileure booking
    - max_booking_confirmation_time - max time booking can be confirmed
    - threshold_time - if booking is made this day until time value from threshold_time it will be confirmed in this function
    """
    # rdb.set_trace()
    booking_list = Booking.objects.filter(booking_date__booking_date=datetime.datetime.now().date())
    term_kayaks = TermKayaks.objects.all()
    active = []
    waiting_for_active = []
    inactive = []
    canceled = []
    kayaks_returned = []
    today = datetime.datetime.now().date()
    current_time = datetime.datetime.now().time()
    start_activation = datetime.time(7)
    stop_activation = datetime.time(9)
    phone_check_activation = datetime.time(9, 30)
    for booking in booking_list:
        if booking.exact_time.time() < start_activation and booking.exact_time.date() <= today:
            if booking.active is True:
                active.append('Booking {} ACTIVE'.format(booking.code))
            else:
                if start_activation <= current_time <= stop_activation:
                    waiting_for_active.append(
                        'Booking {} WAITING FOR ACTIVE'.format(booking.code))
                elif stop_activation < current_time < phone_check_activation:
                    inactive.append('Rezerwacja {} INACTIVE - phone call check'.format(booking.code))
                elif current_time >= phone_check_activation:
                    canceled.append('Booking {} CANCELED'.format(booking.code))
                    for detail in term_kayaks:
                        if detail.booking.active is False and booking.id == detail.booking_id:
                            detail.kayak.store += detail.quantity
                            detail.kayak.save()
                            kayaks_returned.append(
                                'Dodano {} sztuk {} do stanu z zamowienia {}'.format(detail.quantity,
                                                                                     detail.kayak.name,
                                                                                     detail.booking.code))

    return list(dict.fromkeys(active)), list(
        dict.fromkeys(waiting_for_active)), list(
        dict.fromkeys(inactive)), list(
        dict.fromkeys(canceled)), kayaks_returned



"""
celery -A wanplac_project  worker --loglevel=info -P solo

celery -A wanplac_project beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

"""