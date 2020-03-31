from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet
from app2.models import Booking, TermKayaks


class BookingCreateForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['user']


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
        for form in self.forms:
            quantity = form.cleaned_data['quantity']
            kayak = form.cleaned_data['kayak']
            if quantity == 0:
                raise forms.ValidationError('Ilość wybranych kajaków nie może być równa 0.')
            if quantity > kayak.store:
                raise forms.ValidationError('Ilość wybranych kajaków ({}) nie może być większa od ilości dostępnych kajaków ({}).'.format(quantity, kayak.store))


class TermKayaksForm(forms.ModelForm):
    class Meta:
        model = TermKayaks
        exclude = ['booking']


TermKayaksFormSet = inlineformset_factory(
    Booking, TermKayaks, form=TermKayaksForm, formset=CustomFormSet,
    fields=['kayak', 'quantity'], extra=1, can_delete=True, max_num=5, validate_max=True
)
