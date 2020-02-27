from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory, DateInput

from client_panel.models import Booking, BookingKayaks


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


class BookingKayaksForm(forms.ModelForm):

    class Meta:
        model = BookingKayaks
        exclude = ['booking']


BookingKayaksFormSet = inlineformset_factory(
    Booking, BookingKayaks, form=BookingKayaksForm,
    fields=['kayak', 'quantity'], extra=1, can_delete=True
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


