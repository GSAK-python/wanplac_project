from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app1.forms import BookingCreateForm, DailyKayakBookingFormSet
from app1.models import Booking


class DailyBookingCreateView(CreateView):
    model = Booking
    template_name = 'app1/booking/create2.html'
    form_class = BookingCreateForm
    success_url = reverse_lazy('registration:login')

    def get_context_data(self, **kwargs):
        data = super(DailyBookingCreateView, self).get_context_data(**kwargs)

        if self.request.POST:
            data['daily_kayak'] = DailyKayakBookingFormSet(self.request.POST, instance=self.object, prefix='daily_kayak')
        else:
            data['daily_kayak'] = DailyKayakBookingFormSet(instance=self.object, prefix='daily_kayak')

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        daily_kayak = context['daily_kayak']
        with transaction.atomic():
            if not form.cleaned_data['first_name']:
                form.instance.first_name = self.request.user.first_name
            if not form.cleaned_data['last_name']:
                form.instance.last_name = self.request.user.last_name

            form.instance.user = self.request.user
            booking_form = form.save()
            if daily_kayak.is_valid():
                daily_kayak.instance = booking_form
                daily_kayak.save()
        return super(DailyBookingCreateView, self).form_valid(form)
