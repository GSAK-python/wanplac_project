from celery.contrib import rdb
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory, TextInput

from client_panel.models import Booking, TermKayaks, DateList


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
        exclude = ['user']
        # widgets = {
        #     'date': TextInput(attrs={'readonly':'readonly'})
        # }


class TermKayaksForm(forms.ModelForm):
    class Meta:
        model = TermKayaks
        exclude = ['booking']


TermKayaksFormSet = inlineformset_factory(
    Booking, TermKayaks, form=TermKayaksForm,
    fields=['kayak', 'quantity'], extra=1, can_delete=True, max_num=5
)


class SignUpCreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, help_text='IMIĘ')
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=128)
    error_messages = {
        'password_mismatch': 'Podane hasła nie są takie same.',
    }

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']
        help_texts = {
            'username': '150 znaków lub mniej. Litery, cyfry oraz @/./+/-/_ ',
        }



