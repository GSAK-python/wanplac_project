import datetime
from celery.contrib import rdb
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
import app1
import app2
import client_panel
from client_panel.models import DateList
from app2.models import DateList
from app1.models import DateList


class MainPageView(TemplateView):
    template_name = 'main_page/main.html'


class AboutUsView(TemplateView):
    template_name = 'main_page/about_us.html'


class FAQView(TemplateView):
    template_name = 'main_page/FAQ.html'


class ContactView(TemplateView):
    template_name = 'main_page/contact.html'


class RouteView(TemplateView):
    template_name = 'main_page/route.html'

    def get_context_data(self, **kwargs):
        context = super(RouteView, self).get_context_data()
        context['route'] = client_panel.models.Route.objects.all()
        return context


class KayaksView(TemplateView):
    template_name = 'main_page/kayaks.html'

    def get_context_data(self, **kwargs):
        context = super(KayaksView, self).get_context_data()
        context['kayak'] = client_panel.models.Kayak.objects.all()
        return context


class ChooseDateView(LoginRequiredMixin, TemplateView):
    template_name = 'main_page/choose_date.html'

    def get_context_data(self, **kwargs):
        context = super(ChooseDateView, self).get_context_data(**kwargs)
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


class BookingListView(LoginRequiredMixin, ListView):
    template_name = 'main_page/my_booking.html'
    queryset = app1.models.Booking.objects.all()

    def get_context_data(self, **kwargs):
        # rdb.set_trace()
        context = super(BookingListView, self).get_context_data()
        my_booking_app1 = app1.models.Booking.objects.filter(user=self.request.user)
        my_kayak_app1 = app1.models.TermKayaks.objects.filter(booking__user=self.request.user)
        my_booking_app2 = app2.models.Booking.objects.filter(user=self.request.user)
        my_kayak_app2 = app2.models.TermKayaks.objects.filter(booking__user=self.request.user)
        my_booking_client_panel = client_panel.models.Booking.objects.filter(user=self.request.user)
        my_kayak_client_panel = client_panel.models.TermKayaks.objects.filter(booking__user=self.request.user)
        my_date_app1 = app1.models.BookingDate.objects.all()
        my_date_app2 = app2.models.BookingDate.objects.all()
        my_date_client_panel = client_panel.models.BookingDate.objects.all()
        union = my_booking_app1.union(my_booking_app2, my_booking_client_panel).order_by('-exact_time')
        context['union'] = union
        context['kayak'] = my_kayak_app2.union(my_kayak_app1, my_kayak_client_panel).distinct('booking_id')
        context['date'] = my_date_app1.union(my_date_app2, my_date_client_panel)
        return context


class BookingDetailView(LoginRequiredMixin, ListView):
    template_name = 'main_page/booking_detail.html'
    queryset = app1.models.Booking.objects.all()

    def get_context_data(self, **kwargs):
        data = super(BookingDetailView, self).get_context_data()
        my_booking_app1 = app1.models.Booking.objects.filter(user=self.request.user)
        my_kayak_app1 = app1.models.TermKayaks.objects.filter(booking__user=self.request.user)
        my_booking_app2 = app2.models.Booking.objects.filter(user=self.request.user)
        my_kayak_app2 = app2.models.TermKayaks.objects.filter(booking__user=self.request.user)
        my_booking_client_panel = client_panel.models.Booking.objects.filter(user=self.request.user)
        my_kayak_client_panel = client_panel.models.TermKayaks.objects.filter(booking__user=self.request.user)
        union = my_booking_app1.union(my_booking_app2, my_booking_client_panel).latest('exact_time')
        my_date_app1 = app1.models.BookingDate.objects.all()
        my_date_app2 = app2.models.BookingDate.objects.all()
        my_date_client_panel = client_panel.models.BookingDate.objects.all()
        data['union'] = union
        data['kayak'] = my_kayak_app2.union(my_kayak_app1, my_kayak_client_panel).distinct('booking_id')
        data['date'] = my_date_app1.union(my_date_app2, my_date_client_panel)
        return data
