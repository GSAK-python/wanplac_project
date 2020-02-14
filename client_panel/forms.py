from django import forms
from client_panel.models import Booking


class BookingCreateForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['user']
