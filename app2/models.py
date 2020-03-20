import datetime
from celery.contrib import rdb
from django.contrib.auth.models import User
from django.db import models


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


def get_date():
    # rdb.set_trace()
    current_day = datetime.datetime.now().date()
    next_next_day = datetime.datetime.now().date() + datetime.timedelta(days=2)
    day_list = DateList.objects.values_list('date', flat=True)
    for day in day_list:
        if day == current_day:
            display_day = day
        else:
            display_day = next_next_day
        return display_day


def set_date():
    # rdb.set_trace()
    # obj = DateList.objects.first()
    # obj.refresh_from_db_lazy()
    return datetime.datetime.now().date()


class Booking(models.Model):
    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)
    time = models.TimeField()
    date = models.DateField(default=DateList.objects.values_list('date', flat=True)[0])  # datetime.datetime.now().date()
    user = models.ForeignKey(User, related_name='user_app2', on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.date == datetime.datetime.now().date() and datetime.datetime.now().time() < datetime.time(12):
            self.date = datetime.datetime.now().date()
        elif self.date == datetime.datetime.now().date() and datetime.datetime.now().time() >= datetime.time(12):
            self.date = datetime.datetime.now().date() + datetime.timedelta(days=2)
        super(Booking, self).save(*args, **kwargs)

    def __str__(self):
        return 'Rezerwacja: {} {}, Trasa: {}, Godzina {}'.format(self.first_name,
                                                                 self.last_name,
                                                                 self.route,

                                                                 self.time)


class TermKayaks(models.Model):
    booking = models.ForeignKey(Booking, related_name='app2_term_bookings', on_delete=models.CASCADE)
    kayak = models.ForeignKey(Kayak, related_name='app2_kayaks', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)