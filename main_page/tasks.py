from __future__ import absolute_import, unicode_literals
import datetime
from celery import shared_task
from celery.contrib import rdb
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.html import strip_tags

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


@shared_task
def send_reminder_mail():
    # rdb.set_trace()
    my_booking_app1 = app1.models.Booking.objects.all()
    my_booking_app2 = Booking.objects.all()
    my_booking_client_panel = client_panel.models.Booking.objects.all()
    current_day = datetime.datetime.now().date()
    booking_reminder_list = []

    for booking in my_booking_client_panel:
        if booking.booking_date.booking_date == current_day:
            booking_reminder_list.append(booking.user.email)

    for booking in my_booking_app1:
        if booking.booking_date.booking_date == current_day:
            booking_reminder_list.append(booking.user.email)

    for booking in my_booking_app2:
        if booking.booking_date.booking_date == current_day:
            booking_reminder_list.append(booking.user.email)

    subject, from_email, to = 'Przypomnienie o potwierdzeniu rezerwacji - Wan-Plac Krutyń', 'wanplac.rezerwacjen@gmail.com', booking_reminder_list
    html_content = render_to_string('reminder_email.html')
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, from_email, bcc=booking_reminder_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return "Reminder email send for bookings : {}".format(booking_reminder_list)
