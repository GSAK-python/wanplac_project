import datetime
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
        return 'Data: {}'.format(self.date)


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
        return '{}. Dostępnosc {}'.format(self.name, self.store)


class Route(models.Model):
    name = models.CharField(max_length=32)
    distance = models.CharField(max_length=32)
    description = models.TextField()

    def __str__(self):
        return 'Trasa {}, dystans: {}'.format(self.name, self.distance)


def get_date():
    return 'Dont delete me'


def booking_dates_limit():
    # rdb.set_trace()
    current_day = datetime.datetime.now().date()
    booking_dates_list = BookingDate.objects.values_list('booking_date', flat=True)
    current_time = datetime.datetime.now().time()
    change_time = datetime.time(12)
    if current_day in booking_dates_list:
        if current_time < change_time:
            return {'booking_date__exact': datetime.datetime.now().date()}
        elif current_time >= change_time:
            return {'booking_date__gt': datetime.datetime.now().date()}
    else:
        return {'booking_date__gt': datetime.datetime.now().date()}


class Booking(models.Model):
    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)
    time = models.TimeField()
    booking_date = models.ForeignKey(BookingDate, on_delete=models.CASCADE, limit_choices_to=booking_dates_limit,
                                     default='')
    user = models.ForeignKey(User, related_name='user_app2', on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)

    def __str__(self):
        return 'Rezerwacja: {} {}, Trasa: {}, Godzina {}'.format(self.first_name,
                                                                 self.last_name,
                                                                 self.route,
                                                                 self.time)


class TermKayaks(models.Model):
    booking = models.ForeignKey(Booking, related_name='app2_term_bookings', on_delete=models.CASCADE)
    kayak = models.ForeignKey(Kayak, related_name='app2_kayaks', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)