import datetime

from celery.contrib import rdb
from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet
from app1.models import Booking, TermKayaks


class BookingConfirmForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['active', 'code']

    def clean(self):
        super(BookingConfirmForm, self).clean()
        active = self.cleaned_data['active']
        if active is False:
            raise forms.ValidationError('Zaznacz aby aktywować rezerwacje.')


class BookingCreateForm(forms.ModelForm):

    class Meta:
        model = Booking
        exclude = ['user', 'email', 'code']

    def clean(self):
        # rdb.set_trace()
        super(BookingCreateForm, self).clean()
        phone = self.cleaned_data['phone']
        eu_country_code = ['48', '43', '32', '420', '45', '358', '33', '49', '39', '31', '47', '46', '7', '380']
        eu_number_leght_9 = ['32', '33', '31', '48']
        eu_number_leght_10 = ['358', '7']
        eu_number_leght_10_11 = ['43', '49']
        eu_country_code_7_10 = ['420', '45', '39', '47', '46', '380']
        if len(phone) != 9:
            raise forms.ValidationError('Nieprawiodłowa długość numeru telefonu.')
        # for code in eu_country_code:
        #     if not phone.startswith(code):
        #         raise forms.ValidationError('Nieprawidłowy numer kierunkowy ({})'.format(phone[:2]))


class TermKayaksForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TermKayaksForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].initial = 1

    class Meta:
        model = TermKayaks
        exclude = ['booking', 'user']


class CustomFormSet(BaseInlineFormSet):
    
    def full_clean(self):
        super(CustomFormSet, self).full_clean()
        for error in self._non_form_errors.as_data():
            if error.code == 'too_many_forms':
                error.message = "Maksymalna ilość dodatkowych pól z kajakami to %d." % self.max_num

    def clean(self):
        # rdb.set_trace()
        if any(self.errors):
            return
        kayak_list = []
        for form in self.forms:
            quantity = form.cleaned_data['quantity']
            kayak = form.cleaned_data['kayak']
            if quantity == 0:
                raise forms.ValidationError('Ilość wybranych kajaków nie może być równa 0.')
            if quantity > kayak.store:
                raise forms.ValidationError('Ilość wybranych kajaków ({}) nie może być większa od ilości dostępnych kajaków ({}).'.format(quantity, kayak.store))
            kayak_list.append(kayak.name)
        if len(set(kayak_list)) != len(kayak_list):
            raise forms.ValidationError('Taki sam rodzaj kajaka w więcej niż jednym wierszu')


"""
max_num - depends on how amny kayaks type we want to rent
"""
TermKayaksFormSet = inlineformset_factory(
    Booking, TermKayaks, form=TermKayaksForm, formset=CustomFormSet,
    fields=['kayak', 'quantity'], extra=1, can_delete=True, max_num=5, validate_max=True

)
