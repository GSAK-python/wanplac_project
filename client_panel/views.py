from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import CreateView
from client_panel.forms import BookingCreateForm, SignUpCreateForm, TermKayaksFormSet, LoginCreateForm
from client_panel.models import Booking
from client_panel.tasks import check_quantity_kayak
from main_page.views import MainPageView


class Login(LoginView):
    template_name = 'registration/login.html'
    form_class = LoginCreateForm

    def form_valid(self, form):
        check_quantity_kayak.delay()
        return super(Login, self).form_valid(form)


class Logout(LogoutView):
    next_page = '/'


class BookingCreateView(CreateView):
    model = Booking
    template_name = 'client_panel/booking/create.html'
    form_class = BookingCreateForm
    success_url = reverse_lazy('registration:login')

    def get_context_data(self, **kwargs):
        data = super(BookingCreateView, self).get_context_data(**kwargs)

        if self.request.POST:
            data['kayak_set'] = TermKayaksFormSet(self.request.POST, instance=self.object, prefix='kayak_set')
        else:
            data['kayak_set'] = TermKayaksFormSet(instance=self.object, prefix='kayak_set')

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        kayak_set = context['kayak_set']
        with transaction.atomic():
            if not form.cleaned_data['first_name']:
                form.instance.first_name = self.request.user.first_name
            if not form.cleaned_data['last_name']:
                form.instance.last_name = self.request.user.last_name

            form.instance.user = self.request.user
            booking_form = form.save()
            if kayak_set.is_valid():
                kayak_set.instance = booking_form
                kayak_set.save()
                for detail in kayak_set.instance.term_bookings.all():
                    detail.kayak.store -= detail.quantity
                    if not detail.kayak.store:
                        detail.kayak.available = False
                    detail.kayak.save()
        return super(BookingCreateView, self).form_valid(form)


class SignUpCreateView(CreateView):
    model = UserCreationForm
    template_name = 'registration/signup_form.html'
    form_class = SignUpCreateForm

    def form_valid(self, form):
        return super(SignUpCreateView, self).form_valid(form)


