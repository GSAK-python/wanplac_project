from celery.contrib import rdb
from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, BaseInlineFormSet
from django.utils.translation import gettext_lazy as _
from app1.models import Booking, TermKayaks, Kayak


class BookingCreateForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['user']


class TermKayaksForm(forms.ModelForm):
    class Meta:
        model = TermKayaks
        exclude = ['booking']


class CustomFormSet(BaseInlineFormSet):
    def clean(self):
        # rdb.set_trace()
        if any(self.errors):
            return
        for form in self.forms:
            quantity = form.cleaned_data['quantity']
            kayak = form.cleaned_data['kayak']
            if quantity > kayak.store:
                raise forms.ValidationError('Ilość wybranych kajaków nie może być większa od ilości dostępnych kajaków')


TermKayaksFormSet = inlineformset_factory(
    Booking, TermKayaks, form=TermKayaksForm, formset=CustomFormSet,
    fields=['kayak', 'quantity'], extra=1, can_delete=True
)
