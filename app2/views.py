import datetime

from celery.contrib import rdb
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView
from app2.forms import BookingCreateForm, TermKayaksFormSet
from app2.models import Booking, DateList


class BookingCreateView(CreateView):
    model = Booking
    template_name = 'app2/booking/create_app2.html'
    form_class = BookingCreateForm
    success_url = reverse_lazy('registration:login')

    def get_context_data(self, **kwargs):
        data = super(BookingCreateView, self).get_context_data(**kwargs)
        data['current_time'] = datetime.datetime.now().time()
        data['start_break'] = datetime.time(12)
        data['stop_break'] = datetime.time(12, 30)
        data['app1_date_list'] = DateList.objects.values_list('date', flat=True)
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
        current_time = context['current_time']
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
                for detail in kayak_set.instance.app2_term_bookings.all():
                    detail.kayak.store -= detail.quantity
                    if not detail.kayak.store:
                        detail.kayak.available = False
                    detail.kayak.save()
                return super(BookingCreateView, self).form_valid(form)

        return super(BookingCreateView, self).form_invalid(form)