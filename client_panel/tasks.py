from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.contrib import rdb
import datetime
from datetime import time
from client_panel.models import Booking, Kayak, DateList, TermKayaks


@shared_task
def check_quantity_kayak():
    # rdb.set_trace()
    now = datetime.date.today()
    yesterday = now - datetime.timedelta(days=1)

    queryset = Booking.objects.filter(date__endswith=yesterday)
    d = {}
    for query in queryset:
        for item in query.kayak_set.all():
            if item.kayak.name not in d:
                d[item.kayak.name] = item.quantity
            else:
                d[item.kayak.name] += item.quantity

    for name, quantity in d.items():
        object = Kayak.objects.get(name=name)
        object.quantity += quantity
        object.save()

    return 'Baza zauktalizowana: {} kajaki wróciły do nas!'.format(sum(d.values()))


@shared_task
def add(x, y):
    result = x + y
    return result


@shared_task
def check_booking_status():
    # rdb.set_trace()
    kayak_list = Kayak.objects.all()
    days_list = DateList.objects.values_list('date', flat=True)
    current_time = datetime.datetime.now().time()
    t1 = datetime.time(14, 45)
    t2 = datetime.time(15, 55)
    for day in days_list:
        if day == datetime.datetime.now().date() and current_time < t1:
            return True
        if day == datetime.datetime.now().date() and (t1 <= current_time <= t2):
            for kayak in kayak_list:
                kayak.store = kayak.stock
                kayak.save()
            return True
    return False


@shared_task
def check_kayak_status():
    if check_booking_status() is True:
        kayak_list = Kayak.objects.all()
        result_list = []
        for kayak in kayak_list:
            result = '{}'.format(kayak)
            result_list.append(result)

        return result_list
    return 'Rezerwacja kajakow zostala zakonczona'


"""
celery -A wanplac_project  worker --loglevel=info -P solo
"""
