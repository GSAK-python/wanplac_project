from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from client_panel.forms import BookingCreateForm, SignUpCreateForm, LoginCreateForm
from client_panel.models import Booking


class Login(LoginView):
    template_name = 'registration/login.html'
    form_class = LoginCreateForm
    
    def form_valid(self, form):
        return super(Login, self).form_valid(form)


class Logout(LogoutView):
    next_page = '/'


class BookingCreateView(CreateView):
    model = Booking
    template_name = 'booking/create.html'
    form_class = BookingCreateForm
    success_url = reverse_lazy('booking:create')

    def form_valid(self, form):
        form.instance.user = self.request.user
        if form.is_valid():
            booking = form.save(commit=False)
            booking.save()
            return super(BookingCreateView, self).form_valid(form)


class SignUpCreateView(CreateView):
    model = UserCreationForm
    template_name = 'registration/signup_form.html'
    form_class = SignUpCreateForm

    def form_valid(self, form):
        return super(SignUpCreateView, self).form_valid(form)



