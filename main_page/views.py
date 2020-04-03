import datetime

from celery.contrib import rdb
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView
import app1
import app2
import client_panel
from client_panel.models import DateList
from app2.models import DateList
from app1.models import DateList


class MainPageView(TemplateView):
    template_name = 'main_page/main.html'

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        if self.request:
            context['current_day'] = datetime.datetime.now().date()
            context['next_day'] = datetime.datetime.now().date() + datetime.timedelta(days=1)
            context['next_next_day'] = datetime.datetime.now().date() + datetime.timedelta(days=2)
            context['next_next_next_day'] = datetime.datetime.now().date() + datetime.timedelta(days=3)
            context['client_panel_date_list'] = client_panel.models.DateList.objects.values_list('date', flat=True)
            context['app2_date_list'] = app2.models.DateList.objects.values_list('date', flat=True)
            context['app1_date_list'] = app1.models.DateList.objects.values_list('date', flat=True)
            context['current_time'] = datetime.datetime.now().time()
            context['start_break'] = datetime.time(11, 45)
            context['stop_break'] = datetime.time(12, 15)
            return context


class BookingListView(ListView):
    template_name = 'main_page/my_booking.html'
    queryset = app1.models.Booking.objects.all()

    def get_context_data(self, **kwargs):
        # rdb.set_trace()
        context = super(BookingListView, self).get_context_data()
        # context['my_booking_app1'] = app1.models.Booking.objects.filter(user=self.request.user)
        # context['my_kayak_app1'] = app1.models.TermKayaks.objects.filter(booking__user=self.request.user)
        # context['my_booking_app2'] = app2.models.Booking.objects.filter(user=self.request.user)
        # context['my_kayak_app2'] = app2.models.TermKayaks.objects.filter(booking__user=self.request.user)
        # context['my_booking_client_panel'] = client_panel.models.Booking.objects.filter(user=self.request.user)
        # context['my_kayak_client_panel'] = client_panel.models.TermKayaks.objects.filter(booking__user=self.request.user)
        my_booking_app1 = app1.models.Booking.objects.filter(user=self.request.user)
        my_kayak_app1 = app1.models.TermKayaks.objects.filter(booking__user=self.request.user)
        my_booking_app2 = app2.models.Booking.objects.filter(user=self.request.user)
        my_kayak_app2 = app2.models.TermKayaks.objects.filter(booking__user=self.request.user)
        my_booking_client_panel = client_panel.models.Booking.objects.filter(user=self.request.user)
        my_kayak_client_panel = client_panel.models.TermKayaks.objects.filter(booking__user=self.request.user)
        my_booking_list = [my_booking_app1, my_booking_app2, my_booking_client_panel]
        my_kayak_list = [my_kayak_app1, my_kayak_app2, my_kayak_client_panel]
        # context['my_booking_list'] = my_booking_list
        # context['my_kayak_list'] = my_kayak_list
        union = my_booking_app1.union(my_booking_app2, my_booking_client_panel).order_by('-exact_time')
        context['union'] = union
        context['kayak'] = my_kayak_app2.union(my_kayak_app1, my_kayak_client_panel).distinct('booking_id')
        return context
