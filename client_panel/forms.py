from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from client_panel.models import Booking


class BookingCreateForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['user']


class SignUpCreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, help_text='IMIĘ')
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=128)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']
        help_texts = {
            'first_name': 'Podaj swoje imię'
        }


