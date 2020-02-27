from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView
from client_panel.forms import BookingCreateForm, SignUpCreateForm, LoginCreateForm, BookingKayaksFormSet
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

    def get_context_data(self, **kwargs):
        data = super(BookingCreateView, self).get_context_data(**kwargs)

        if self.request.POST:
            data['reservation'] = BookingKayaksFormSet(self.request.POST, instance=self.object)
        else:
            data['reservation'] = BookingKayaksFormSet(instance=self.object)

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        booking_form = context['reservation']
        with transaction.atomic():
            if not form.cleaned_data['first_name']:
                form.instance.first_name = self.request.user.first_name
            if not form.cleaned_data['last_name']:
                form.instance.last_name = self.request.user.last_name

            form.instance.user = self.request.user
            reservation = form.save()
            if booking_form.is_valid():
                booking_form.instance = reservation
                booking_form.save()
                for form in booking_form:
                    booking = form.save(commit=False)
                    booking_form.reservation = reservation
                    booking.save()
        return super(BookingCreateView, self).form_valid(form)


class SignUpCreateView(CreateView):
    model = UserCreationForm
    template_name = 'registration/signup_form.html'
    form_class = SignUpCreateForm

    def form_valid(self, form):
        return super(SignUpCreateView, self).form_valid(form)
