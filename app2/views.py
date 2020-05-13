import datetime
from celery.contrib import rdb
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.html import strip_tags
from django.views.generic import CreateView, UpdateView
from app2.forms import BookingCreateForm, TermKayaksFormSet, BookingConfirmForm
from app2.models import Booking, BookingDate


class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    template_name = 'app2/booking/create_app2.html'
    form_class = BookingCreateForm
    success_url = reverse_lazy('main:booking_detail')

    def get_context_data(self, **kwargs):
        data = super(BookingCreateView, self).get_context_data(**kwargs)
        data['current_time'] = datetime.datetime.now().time()
        data['start_break'] = datetime.time(12)
        data['stop_break'] = datetime.time(12, 30)
        data['current_day'] = datetime.datetime.now().date()
        data['today_users'] = Booking.objects.values_list('user', flat=True)
        data['date'] = BookingDate.objects.last()

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
        today_users = context['today_users']
        date = context['date']
        with transaction.atomic():
            if not form.cleaned_data['first_name']:
                form.instance.first_name = self.request.user.first_name
            if not form.cleaned_data['last_name']:
                form.instance.last_name = self.request.user.last_name
            form.instance.user = self.request.user
            form.instance.email = self.request.user.email
            today_users_list = []
            for user in today_users:
                today_users_list.append(user)
            if form.instance.user_id in today_users_list and date.id == form.instance.booking_date.id:
                messages.add_message(self.request, messages.INFO,
                                     'Użytkownik może mieć tylko jedną rezerwację na dzień.')
                return super(BookingCreateView, self).form_invalid(form)
            if kayak_set.is_valid():
                booking_form = form.save()
                if datetime.time(7) <= booking_form.exact_time.time() <= datetime.time(
                        12) and booking_form.booking_date.booking_date == current_day:
                    booking_form.active = True
                    booking_form.save()
                kayak_set.instance = booking_form
                kayak_set.save()
                for detail in kayak_set.instance.app2_term_bookings.all():
                    detail.kayak.store -= detail.quantity
                    if not detail.kayak.store:
                        detail.kayak.available = False
                    detail.kayak.save()

                subject, from_email, to = 'Rezerwacja kajaków - Wan-Plac Krutyń', 'wanplac.rezerwacjen@gmail.com', self.request.user.email
                html_content = render_to_string('booking_email.html', {'detail': detail,
                                                                       'kayak': kayak_set.instance.app2_term_bookings.all(),
                                                                       })
                text_content = strip_tags(html_content)
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                return super(BookingCreateView, self).form_valid(form)

        return super(BookingCreateView, self).form_invalid(form)


class App2BookingConfirmationView(LoginRequiredMixin, UpdateView):
    template_name = 'app2/booking/booking_confirmation.html'
    form_class = BookingConfirmForm
    success_url = reverse_lazy('main:thanks')
    model = Booking

    def get_context_data(self, **kwargs):
        context = super(App2BookingConfirmationView, self).get_context_data(**kwargs)
        context['current_time'] = datetime.datetime.now().time()
        context['threshold_time'] = datetime.time(7)
        context['max_booking_confirm_time'] = datetime.time(9)
        context['booking_cancel_info'] = datetime.time(12, 30)
        return context

    def get_object(self, queryset=None):
        booking = Booking.objects.filter(user=self.request.user).last()
        return booking
