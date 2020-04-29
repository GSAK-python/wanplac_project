import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.html import strip_tags
from django.views.generic import CreateView
from client_panel.forms import BookingCreateForm, SignUpCreateForm, TermKayaksFormSet, LoginCreateForm
from client_panel.models import Booking


class Login(LoginView):
    template_name = 'registration/login.html'
    form_class = LoginCreateForm

    def form_valid(self, form):
        # check_quantity_kayak.delay()
        return super(Login, self).form_valid(form)


class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    template_name = 'client_panel/booking/create.html'
    form_class = BookingCreateForm
    success_url = reverse_lazy('main:booking_detail')

    def get_context_data(self, **kwargs):
        data = super(BookingCreateView, self).get_context_data(**kwargs)
        data['current_time'] = datetime.datetime.now().time()
        data['start_break'] = datetime.time(12)
        data['stop_break'] = datetime.time(12, 30)

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
            form.instance.email = self.request.user.email
            if kayak_set.is_valid():
                booking_form = form.save()
                kayak_set.instance = booking_form
                kayak_set.save()
                for detail in kayak_set.instance.term_bookings.all():
                    detail.kayak.store -= detail.quantity
                    if not detail.kayak.store:
                        detail.kayak.available = False
                    detail.kayak.save()

                subject, from_email, to = 'Rezerwacja kajaków - Wan-Plac Krutyń', 'gsak.python@gmail.com', self.request.user.email
                html_content = render_to_string('booking_email.html', {'detail': detail, 'kayak': kayak_set.instance.term_bookings.all()})
                text_content = strip_tags(html_content)
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                return super(BookingCreateView, self).form_valid(form)

        return super(BookingCreateView, self).form_invalid(form)


class SignUpCreateView(CreateView):
    model = UserCreationForm
    template_name = 'registration/signup_form.html'
    form_class = SignUpCreateForm

    def form_valid(self, form):
        subject, from_email, to = 'Utworzenie nowego konta - Wan-Plac Krutyń', 'gsak.python@gmail.com', form.cleaned_data['email']
        html_content = render_to_string('registration/user_data_email.html',
                                        {
                                         'email': form.cleaned_data['email'],
                                         'first_name': form.cleaned_data['first_name'],
                                         'last_name': form.cleaned_data['last_name'],
                                         'username': form.cleaned_data['username']
                                         }
                                        )
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return super(SignUpCreateView, self).form_valid(form)


