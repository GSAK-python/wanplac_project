from django import forms
from django.forms import inlineformset_factory, TextInput

from app2.models import Booking, TermKayaks


class BookingCreateForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['user']
        widgets = {
            'date': TextInput(attrs={'readonly':'readonly'})
        }


class TermKayaksForm(forms.ModelForm):
    class Meta:
        model = TermKayaks
        exclude = ['booking']


TermKayaksFormSet = inlineformset_factory(
    Booking, TermKayaks, form=TermKayaksForm,
    fields=['kayak', 'quantity'], extra=1, can_delete=True, max_num=5
)
