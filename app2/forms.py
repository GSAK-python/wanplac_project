from django import forms
from django.forms import inlineformset_factory

from app2.models import Booking, BookingKayaks, TermKayaks


class BookingCreateForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['user']


class BookingKayaksForm(forms.ModelForm):

    class Meta:
        model = BookingKayaks
        exclude = ['booking']


BookingKayaksFormSet = inlineformset_factory(
    Booking, BookingKayaks, form=BookingKayaksForm,
    fields=['date'], extra=1, can_delete=True, max_num=1
)


class TermKayaksForm(forms.ModelForm):
    class Meta:
        model = TermKayaks
        exclude = ['booking']


TermKayaksFormSet = inlineformset_factory(
    Booking, TermKayaks, form=TermKayaksForm,
    fields=['kayak', 'quantity'], extra=1, can_delete=True, max_num=5
)
