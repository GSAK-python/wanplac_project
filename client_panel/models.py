import datetime

from django.contrib.auth.models import User
from django.db import models


# class Term(models.Model):
#     date = models.DateField()
#
#     def __str__(self):
#         return 'Data: {}'.format(self.date)


class Kayak(models.Model):
    TYPECHOICE = [
        ('Jednosoboy', 'Jednoosobwy'),
        ('Dwuosobowy', 'Dwuosobowy'),
        ('Trzyosobowy', 'Trzyosobowy')
    ]
    name = models.CharField(max_length=32)
    store = models.IntegerField()
    type = models.CharField(max_length=32, choices=TYPECHOICE)
    available = models.BooleanField()
    description = models.TextField()

    def __str__(self):
        return '{} ({})'.format(self.name, self.store)


class Route(models.Model):
    name = models.CharField(max_length=32)
    distance = models.CharField(max_length=32)
    description = models.TextField()

    def __str__(self):
        return 'Trasa {}, dystans: {}'.format(self.name, self.distance)


class Booking(models.Model):
    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)
    time = models.TimeField()
    date = models.CharField(max_length=32, default=datetime.date.today)
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



