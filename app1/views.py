import datetime

from celery.contrib import rdb
from django.db import transaction
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from requests import request

from app1.forms import BookingCreateForm, TermKayaksFormSet
from app1.models import Booking, DateList


class BookingCreateView(CreateView):
    model = Booking
    template_name = 'app1/booking/create_app1.html'
    form_class = BookingCreateForm
    success_url = reverse_lazy('main:my_booking')

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

                return super(BookingCreateView, self).form_valid(form)

        return super(BookingCreateView, self).form_invalid(form)


