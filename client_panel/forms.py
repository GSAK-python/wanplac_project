from django import forms
from django.contrib.auth.models import User

from client_panel.models import Booking


class BookingCreateForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['user']

