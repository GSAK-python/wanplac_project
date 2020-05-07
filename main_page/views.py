import datetime
from typing import Dict, Any

from celery.contrib import rdb
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DeleteView
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

    def get_context_data(self, **kwargs):
        context = super(FAQView, self).get_context_data()
        context['faq'] = client_panel.models.FAQ.objects.all().order_by('id')
        return context


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
        context['kayak'] = client_panel.models.Kayak.objects.all().order_by('type')
        return context


class PriceListView(TemplateView):
    template_name = 'main_page/price_list.html'

    def get_context_data(self, **kwargs):
        context = super(PriceListView, self).get_context_data()
        context['kayak'] = client_panel.models.Kayak.objects.all().order_by('type')
        context['route'] = client_panel.models.Route.objects.all()
        return context


class HowItLooksView(TemplateView):
    template_name = 'main_page/how.html'


class ProfileView(TemplateView):
    template_name = 'main_page/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data()
        context['user'] = User.objects.get(username=self.request.user)
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


class DeleteUserView(DeleteView):
    template_name = 'main_page/user_delete.html'
    success_url = reverse_lazy('main:user_delete_confirmation')

    def get_object(self, queryset=None):
        user_ = self.request.user
        return get_object_or_404(User, username=user_)

    def get_context_data(self, **kwargs):
        context = super(DeleteUserView, self).get_context_data()
        context['user'] = User.objects.get(username=self.request.user)
        return context


class DeleteUserConfirmationView(TemplateView):
    template_name = 'main_page/user_delete_confirmation.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'main_page/privacy_policy.html'

    def get_context_data(self, **kwargs):
        context = super(PrivacyPolicyView, self).get_context_data()
        context['privacy_policy'] = client_panel.models.PrivacyPolicy.objects.all().order_by('id')
        return context


class AdminPanelView(LoginRequiredMixin, TemplateView):
    template_name = 'main_page/admin_panel.html'
    # queryset = app1.models.Booking.objects.all()

    def get_context_data(self, **kwargs):
        context = super(AdminPanelView, self).get_context_data()
        my_booking_app1 = app1.models.Booking.objects.all()
        my_kayak_app1 = app1.models.TermKayaks.objects.all()
        my_booking_app2 = app2.models.Booking.objects.all()
        my_kayak_app2 = app2.models.TermKayaks.objects.all()
        my_booking_client_panel = client_panel.models.Booking.objects.all()
        my_kayak_client_panel = client_panel.models.TermKayaks.objects.all()
        my_date_app1 = app1.models.BookingDate.objects.all()
        my_date_app2 = app2.models.BookingDate.objects.all()
        my_date_client_panel = client_panel.models.BookingDate.objects.all()
        union = my_booking_app1.union(my_booking_app2, my_booking_client_panel)
        context['union'] = union
        context['kayak'] = my_kayak_app2.union(my_kayak_app1, my_kayak_client_panel).distinct('booking_id')
        context['date'] = my_date_app1.union(my_date_app2, my_date_client_panel).order_by('-booking_date')
        context['app1'] = client_panel.models.Booking.objects.all()
        context['app1_current_day'] = app1.models.BookingDate.objects.latest('booking_date')
        context['app1_current_kayak'] = app1.models.Kayak.objects.all().order_by('id')
        context['app2_current_day'] = app2.models.BookingDate.objects.latest('booking_date')
        context['app2_current_kayak'] = app2.models.Kayak.objects.all().order_by('id')
        context['client_panel_current_day'] = client_panel.models.BookingDate.objects.latest('booking_date')
        context['client_panel_current_kayak'] = client_panel.models.Kayak.objects.all().order_by('id')
        context['change_booking_state'] = datetime.time(9)
        context['current_time'] = datetime.datetime.now().time()
        return context
