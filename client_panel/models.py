import datetime
from celery.contrib import rdb
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

from client_panel.code_generator import random_string


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
        ('Jednoosobowy', 'Jednoosobowy'),
        ('Dwuosobowy', 'Dwuosobowy'),
        ('Trzyosobowy', 'Trzyosobowy')
    ]
    name = models.CharField(max_length=32)
    stock = models.IntegerField()
    store = models.IntegerField()
    type = models.CharField(max_length=32, choices=TYPECHOICE)
    available = models.BooleanField()
    description = models.TextField()
    photo = models.ImageField(null=True, blank=True, upload_to='media')
    prize = models.IntegerField()
    weight = models.CharField(max_length=32)
    dimenstions = models.CharField(max_length=64)
    displacement = models.CharField(max_length=64)

    def __str__(self):
        return '{} - dostępnych sztuk: {} '.format(self.name, self.store)


class Route(models.Model):
    name = models.CharField(max_length=32)
    distance = models.CharField(max_length=32)
    description = models.TextField()
    average_time = models.TextField()
    main_points = models.TextField()
    stop_place = models.TextField()
    next_stage = models.TextField()

    def __str__(self):
        return 'Trasa {}, dystans: {}'.format(self.name, self.distance)


def booking_dates_limit():
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
    TIMECHOICE = [
        ('', 'Kliknij'),
        ('9:00', '9:00'),
        ('9:30', '9:30'),
        ('10:00', '10:00'),
        ('10:30', '10:30'),
        ('11:00', '11:00'),
        ('11:30', '11:30'),
        ('12:00', '12:00'),
    ]
    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)
    time = models.CharField(choices=TIMECHOICE, max_length=32, default='')
    booking_date = models.ForeignKey(BookingDate, related_name='cp_booking_date', on_delete=models.CASCADE, limit_choices_to=booking_dates_limit,
                                     default='')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    alphanumeric = RegexValidator('^[0-9]*$', message='Numer telefonu może zawierać tylko cyfry.')
    phone = models.CharField(max_length=13, validators=[alphanumeric])
    email = models.EmailField()
    exact_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    code = models.CharField(max_length=32, default=random_string)
    active = models.BooleanField(default=False)

    def __str__(self):
        return 'Rezerwacja: {} {}, {}, {} Godzina {}'.format(self.first_name,
                                                             self.last_name,
                                                             self.route,
                                                             self.booking_date,
                                                             self.time)


class TermKayaks(models.Model):
    booking = models.ForeignKey(Booking, related_name='term_bookings', on_delete=models.CASCADE)
    kayak = models.ForeignKey(Kayak, related_name='kayaks', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    exact_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.kayak.name)


class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return 'Pytanie: {}'.format(self.question)


class PrivacyPolicy(models.Model):
    title = models.TextField(blank=True, null=True)
    text = models.TextField()

    def __str__(self):
        return '{}'.format(self.text)
