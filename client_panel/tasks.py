from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.contrib import rdb
import datetime
from client_panel.models import Kayak, DateList, BookingDate


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
                    day = current_day + datetime.timedelta(days=2)
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
            day = current_day + datetime.timedelta(days=2)
            new_date = BookingDate.objects.create(booking_date=day)
            new_date.save()
            new_date.refresh_from_db()
            return 'DODANO NOWY DZIEN {}'.format(day)


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
                kayak.available = True
                kayak.save()
            return 'LICZBA KAJAKOW ZOSTALA UZUPELNIONA'


# @shared_task
# def set_proper_date():
#     # rdb.set_trace()
#     days_list = DateList.objects.values_list('date', flat=True)
#     current_day = datetime.datetime.now().date()
#     current_time = datetime.datetime.now().time()
#     next_day = datetime.datetime.now().date() + datetime.timedelta(days=1)
#     next_next_day = datetime.datetime.now().date() + datetime.timedelta(days=2)
#     change_time = datetime.time(10, 40)
#     for day in days_list:
#         if day == current_day and current_time < change_time:
#             display_date = current_day
#             return display_date
#         elif day == current_day and current_time >= change_time:
#             display_date = next_next_day
#             return display_date
#
#
# @shared_task
# def check_quantity_kayak():
#     # rdb.set_trace()
#     now = datetime.date.today()
#     yesterday = now - datetime.timedelta(days=1)
#
#     queryset = Booking.objects.filter(date__endswith=yesterday)
#     d = {}
#     for query in queryset:
#         for item in query.kayak_set.all():
#             if item.kayak.name not in d:
#                 d[item.kayak.name] = item.quantity
#             else:
#                 d[item.kayak.name] += item.quantity
#
#     for name, quantity in d.items():
#         object = Kayak.objects.get(name=name)
#         object.quantity += quantity
#         object.save()
#
#     return 'Baza zauktalizowana: {} kajaki wróciły do nas!'.format(sum(d.values()))
#
#
# @shared_task
# def check_booking_status():
#     # rdb.set_trace()
#     days_list = DateList.objects.values_list('date', flat=True)
#     current_time = datetime.datetime.now().time()
#     current_day = datetime.datetime.now().date()
#     t1 = datetime.time(18, 5)
#     for day in days_list:
#         if day == current_day and current_time < t1:
#             return True
#         elif day == current_day and current_time > t1:
#             day_to_upload = DateList.objects.filter(date__exact=current_day)
#             for object in day_to_upload:
#                 day = current_day + datetime.timedelta(days=2)
#                 object.date = day
#                 object.save()
#             return 'Dzien zostal zaktualizowany'
#
#     return False
#
#
# @shared_task
# def check_kayak_status():
#     if check_booking_status() is True:
#         kayak_list = Kayak.objects.all()
#         result_list = []
#         for kayak in kayak_list:
#             result = '{}'.format(kayak)
#             result_list.append(result)
#
#         return result_list
#     return 'Rezerwacja kajakow zostala zakonczona'
#
#
# @shared_task
# def db_test_func():
#     # rdb.set_trace()
#     kayak_item = Kayak.objects.get(id=1)
#     kayak_item.store += 1
#     kayak_item.save()
#     return 'Dodawanie 1 sztuki co minutę'


"""
celery -A wanplac_project  worker --loglevel=info -P solo

celery -A wanplac_project beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

"""
