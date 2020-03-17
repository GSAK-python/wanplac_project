from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.contrib import rdb
import datetime
from client_panel.models import Booking, Kayak, DateList


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
