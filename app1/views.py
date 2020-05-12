import datetime
from celery.contrib import rdb
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.html import strip_tags
from django.views.generic import CreateView, UpdateView
from app1.forms import BookingCreateForm, TermKayaksFormSet, BookingConfirmForm
from app1.models import Booking, TermKayaks
from django.core.mail import EmailMessage, EmailMultiAlternatives


class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    template_name = 'app1/booking/create_app1.html'
    form_class = BookingCreateForm
    success_url = reverse_lazy('main:booking_detail')

    def get_context_data(self, **kwargs):
        data = super(BookingCreateView, self).get_context_data(**kwargs)
        data['current_time'] = datetime.datetime.now().time()
        data['start_break'] = datetime.time(12)
        data['stop_break'] = datetime.time(12, 30)
        data['current_day'] = datetime.datetime.now().date()

        if self.request.POST:
            data['kayak_set'] = TermKayaksFormSet(self.request.POST, instance=self.object, prefix='kayak_set')
        else:
            data['kayak_set'] = TermKayaksFormSet(instance=self.object, prefix='kayak_set')

        return data

    def form_valid(self, form):
        # rdb.set_trace()
        context = self.get_context_data()
        kayak_set = context['kayak_set']
        current_day = context['current_day']
        with transaction.atomic():
            if not form.cleaned_data['first_name']:
                form.instance.first_name = self.request.user.first_name
            if not form.cleaned_data['last_name']:
                form.instance.last_name = self.request.user.last_name
            form.instance.user = self.request.user
            form.instance.email = self.request.user.email

            if kayak_set.is_valid():
                booking_form = form.save()
                if datetime.time(7) <= booking_form.exact_time.time() <= datetime.time(12) and booking_form.booking_date == current_day:
                    booking_form.active = True
                    booking_form.save()
                kayak_set.instance = booking_form
                kayak_set.save()
                for detail in kayak_set.instance.app1_term_bookings.all():
                    detail.kayak.store -= detail.quantity
                    if not detail.kayak.store:
                        detail.kayak.available = False
                    detail.kayak.save()

                subject, from_email, to = 'Rezerwacja kajaków - Wan-Plac Krutyń', 'gsak.python@gmail.com', self.request.user.email
                html_content = render_to_string('booking_email.html', {'detail': detail,
                                                                       'kayak': kayak_set.instance.app1_term_bookings.all()})
                text_content = strip_tags(html_content)
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                return super(BookingCreateView, self).form_valid(form)

        return super(BookingCreateView, self).form_invalid(form)


class BookingUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'app1/booking/update_app1.html'
    form_class = BookingCreateForm
    success_url = reverse_lazy('main:booking_detail')

    def get_object(self, queryset=None):
        a = Booking.objects.filter(user=self.request.user).latest('id')
        b = TermKayaks.objects.filter(booking__user=self.request.user)
        return a

    def get_context_data(self, **kwargs):
        data = super(BookingUpdateView, self).get_context_data(**kwargs)
        # data['current_time'] = datetime.datetime.now().time()
        # data['start_break'] = datetime.time(12)
        # data['stop_break'] = datetime.time(12, 30)
        data['kayak_set'] = TermKayaksFormSet(queryset=TermKayaks.objects.filter(booking_id=self.get_object().id),
                                              prefix='kayak_set')

        return data

    def form_valid(self, form):
        # rdb.set_trace()
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
                for detail in kayak_set.instance.app1_term_bookings.all():
                    detail.kayak.store -= detail.quantity
                    if not detail.kayak.store:
                        detail.kayak.available = False
                    detail.kayak.save()

                return super(BookingUpdateView, self).form_valid(form)

        return super(BookingUpdateView, self).form_invalid(form)


class App1BookingConfirmationView(LoginRequiredMixin, UpdateView):
    template_name = 'app1/booking/booking_confirmation.html'
    form_class = BookingConfirmForm
    success_url = reverse_lazy('main:thanks')

    def get_context_data(self, **kwargs):
        context = super(App1BookingConfirmationView, self).get_context_data(**kwargs)
        context['app1_booking'] = Booking.objects.filter(user=self.request.user).latest('id')
        context['current_time'] = datetime.datetime.now().time()
        context['threshold_time'] = datetime.time(7)
        context['max_booking_confirm_time'] = datetime.time(9)
        return context

    def get_object(self, queryset=None):
        booking = Booking.objects.filter(user=self.request.user).last()
        return booking
