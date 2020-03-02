from __future__ import absolute_import, unicode_literals

from celery import shared_task
import datetime

from client_panel.models import Booking, Kayak


@shared_task
def check_quantity_kayak():
    now = datetime.date.today()
    yesterday = now - datetime.timedelta(days=1)

    queryset = Booking.objects.filter(term__endswith=yesterday)
    d = {}
    for query in queryset:
        for item in query.booking_set.all():
            if item.kayak.name not in d:
                d[item.kayak.name] = item.quantity
            else:
                d[item.kayak.name] += item.quantity

    for name, quantity in d.items():
        object = Kayak.objects.get(name=name)
        object.quantity += quantity
        object.save()

    return 'Baza zauktalizowana: {} kajaki wróciły do nas!'.format(sum(d.values()))
