from celery.contrib import rdb
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory, BaseInlineFormSet

from client_panel.models import Booking, TermKayaks


class LoginCreateForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            "Wprowadź poprwaną nazwę użytkownika i/lub hasło. Pamiętaj, że ważna "
            "jest wielkość liter."
        ),
        'inactive': 'To konto jest nieaktywne.'
    }

    class Meta:
        model = User
        fields = ['username', 'password']


class BookingCreateForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['user', 'email', 'code']
        # widgets = {
        #     'date': TextInput(attrs={'readonly':'readonly'})
        # }

    def clean(self):
        super(BookingCreateForm, self).clean()
        phone = self.cleaned_data['phone']
        if len(phone) != 9:
            raise forms.ValidationError('Nieprawiodłowa długość numeru telefonu.')


class TermKayaksForm(forms.ModelForm):
    class Meta:
        model = TermKayaks
        exclude = ['booking']


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


TermKayaksFormSet = inlineformset_factory(
    Booking, TermKayaks, form=TermKayaksForm, formset=CustomFormSet,
    fields=['kayak', 'quantity'], extra=1, can_delete=True, max_num=5, validate_max=True
)


class SignUpCreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, help_text='IMIĘ')
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=128)
    privace_policy = forms.BooleanField()
    error_messages = {
        'password_mismatch': 'Podane hasła nie są takie same.',
    }

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']
        help_texts = {
            'username': '150 znaków lub mniej. Litery, cyfry oraz @/./+/-/_ ',
        }



