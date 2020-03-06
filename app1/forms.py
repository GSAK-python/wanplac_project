from django import forms
from django.forms import inlineformset_factory

from app1.models import DailyKayakBooking, Booking


class BookingCreateForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['user']


class DailyKayakBookingForm(forms.ModelForm):
    class Meta:
        model = DailyKayakBooking
        exclude = ['booking']


DailyKayakBookingFormSet = inlineformset_factory(
    Booking, DailyKayakBooking, form=DailyKayakBookingForm,
    fields=['amount', 'quantity'], extra=1, can_delete=True
)