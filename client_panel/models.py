import datetime
from datetime import date

from celery.contrib import rdb
from django.contrib.auth.models import User
from django.db import models


class BookingDate(models.Model):
    booking_date = models.DateField()

    def __str__(self):
        return '{}'.format(self.booking_date)


class DateList(models.Model):
    date = models.DateField()

    def __str__(self):
        return '{}'.format(self.date)


class Kayak(models.Model):
    TYPECHOICE = [
        ('Jednosoboy', 'Jednoosobwy'),
        ('Dwuosobowy', 'Dwuosobowy'),
        ('Trzyosobowy', 'Trzyosobowy')
    ]
    name = models.CharField(max_length=32)
    stock = models.IntegerField()
    store = models.IntegerField()
    type = models.CharField(max_length=32, choices=TYPECHOICE)
    available = models.BooleanField()
    description = models.TextField()

    def __str__(self):
        return '{}. Na stanie {}. Dostępnosc {}'.format(self.name, self.stock, self.store)


class Route(models.Model):
    name = models.CharField(max_length=32)
    distance = models.CharField(max_length=32)
    description = models.TextField()

    def __str__(self):
        return 'Trasa {}, dystans: {}'.format(self.name, self.distance)


def booking_dates_limit():
    current_time = datetime.datetime.now().time()
    change_time = datetime.time(16, 52)
    if current_time < change_time:
        return {'booking_date__exact': datetime.datetime.now().date()}
    elif current_time >= change_time:
        return {'booking_date__gt': datetime.datetime.now().date()}


class Booking(models.Model):
    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)
    time = models.TimeField()
    booking_date = models.ForeignKey(BookingDate, on_delete=models.CASCADE, limit_choices_to=booking_dates_limit, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)

    def __str__(self):
        return 'Rezerwacja: {} {}, Trasa: {}, Godzina {}'.format(self.first_name,
                                                                 self.last_name,
                                                                 self.route,
                                                                 self.time)


class TermKayaks(models.Model):
    booking = models.ForeignKey(Booking, related_name='term_bookings', on_delete=models.CASCADE)
    kayak = models.ForeignKey(Kayak, related_name='kayaks', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)



