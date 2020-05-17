from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.contrib import rdb

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

import app1
import app2
import client_panel
from app2.models import Booking


@shared_task
def change_status(request, pk):
    # rdb.set_trace()
    my_booking_app1 = app1.models.Booking.objects.all()
    my_booking_app2 = Booking.objects.all()
    my_booking_client_panel = client_panel.models.Booking.objects.all()
    for user in my_booking_app1:
        if user.id == pk:
            if user.active is False:
                user.active = True
                user.save()
            else:
                user.active = False
                user.save()
    for user in my_booking_app2:
        if user.id == pk:
            if user.active is False:
                user.active = True
                user.save()
            else:
                user.active = False
                user.save()
    for user in my_booking_client_panel:
        if user.id == pk:
            if user.active is False:
                user.active = True
                user.save()
            else:
                user.active = False
                user.save()
    return HttpResponseRedirect(reverse_lazy('main:thanks'))


@shared_task
def booking_delete(request, pk):
    # rdb.set_trace()
    my_booking_app1 = app1.models.Booking.objects.all()
    my_booking_app2 = Booking.objects.all()
    my_booking_client_panel = client_panel.models.Booking.objects.all()
    my_kayak_app1 = app1.models.TermKayaks.objects.all()
    my_kayak_app2 = app2.models.TermKayaks.objects.all()
    my_kayak_client_panel = client_panel.models.TermKayaks.objects.all()
    for booking in my_booking_app1:
        if booking.id == pk:
            for kayak in my_kayak_app1:
                if kayak.booking_id == pk:
                    kayak.kayak.store += kayak.quantity
                    kayak.kayak.save()
            booking.delete()
    for booking in my_booking_app2:
        if booking.id == pk:
            for kayak in my_kayak_app2:
                if kayak.booking_id == pk:
                    kayak.kayak.store += kayak.quantity
                    kayak.kayak.save()
            booking.delete()
    for booking in my_booking_client_panel:
        if booking.id == pk:
            for kayak in my_kayak_client_panel:
                if kayak.booking_id == pk:
                    kayak.kayak.store += kayak.quantity
                    kayak.kayak.save()
            booking.delete()
    return HttpResponseRedirect(reverse_lazy('main:delete_booking'))