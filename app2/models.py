from celery.contrib import rdb
from django.contrib.auth.models import User
from django.db import models
import datetime

# Create your models here.
from wanplac_project import settings


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
        return '{}. Na stanie {}. Dostępnosc {}'.format(self.name, self.stock, self.store)


class Route(models.Model):
    name = models.CharField(max_length=32)
    distance = models.CharField(max_length=32)
    description = models.TextField()

    def __str__(self):
        return 'Trasa {}, dystans: {}'.format(self.name, self.distance)


def get_current_data():
    # rdb.set_trace()
    date_list = DateList.objects.values_list('date', flat=True)
    current_day = datetime.datetime.now().date()
    next_day = datetime.datetime.now().date() + datetime.timedelta(days=1)
    next_next_day = datetime.datetime.now().date() + datetime.timedelta(days=2)
    current_time = datetime.datetime.now().time()
    change_time = datetime.time(10, 15)
    if current_day in date_list and current_time < change_time:
        day = current_day
        return day
    elif current_day in date_list and current_time >= change_time:
        day = next_next_day
        return day
    elif current_day not in date_list:
        day = next_day
        return day


class Booking(models.Model):
    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)
    time = models.TimeField()
    date = models.CharField(max_length=32, default=get_current_data())
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
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)