from django.contrib.auth.models import User
from django.db import models


class Term(models.Model):
    date = models.DateField()

    def __str__(self):
        return 'Data: {}'.format(self.date)


class DailyKayak(models.Model):
    date = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="term")
    finder = models.IntegerField()
    eoli = models.IntegerField()
    protour = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.date)


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
    user = models.ForeignKey(User, related_name='user_app1', on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)

    def __str__(self):
        return 'Rezerwacja: {} {}, Trasa: {}, Godzina {}'.format(self.first_name,
                                                                 self.last_name,
                                                                 self.route,
                                                                 self.time)


class DailyKayakBooking(models.Model):
    booking = models.ForeignKey(Booking, related_name='daily_booking', on_delete=models.CASCADE)
    amount = models.ForeignKey(DailyKayak, related_name='amount', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()