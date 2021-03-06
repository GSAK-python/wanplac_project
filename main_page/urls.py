from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

import app2
from app1.views import App1BookingConfirmationView
from app2.views import App2BookingConfirmationView
from client_panel.views import CPBookingConfirmationView
from main_page import tasks
from main_page.views import MainPageView, BookingListView, ChooseDateView, BookingDetailView, AboutUsView, ContactView, \
    FAQView, RouteView, KayaksView, PriceListView, HowItLooksView, ProfileView, DeleteUserView, \
    DeleteUserConfirmationView, PrivacyPolicyView, AdminPanelView, BookingSuccessfulConfirmationView, \
    BookingPlaceHolderView, BookingDeleteView

app_name = 'main'

urlpatterns = [
    path('', MainPageView.as_view(), name='main'),
    path('booking_confirmation/', BookingDetailView.as_view(), name='booking_detail'),
    path('my_booking/', BookingListView.as_view(), name='my_booking'),
    path('choose_date', ChooseDateView.as_view(), name='choose_date'),
    path('about_us', AboutUsView.as_view(), name='about_us'),
    path('FAQ', FAQView.as_view(), name='faq'),
    path('contact', ContactView.as_view(), name='contact'),
    path('route', RouteView.as_view(), name='route'),
    path('kayaks', KayaksView.as_view(), name='kayaks'),
    path('price_list', PriceListView.as_view(), name='price_list'),
    path('how', HowItLooksView.as_view(), name='how'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('user_delete', DeleteUserView.as_view(), name='user_delete'),
    path('user_delete_confirmation', DeleteUserConfirmationView.as_view(), name='user_delete_confirmation'),
    path('privacy_policy', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('qzxwce1928', AdminPanelView.as_view(), name='admin_panel'),
    path('thanks', BookingSuccessfulConfirmationView.as_view(), name='thanks'),
    path('confirm', BookingPlaceHolderView.as_view(), name='confirm'),
    path('delete_booking', BookingDeleteView.as_view(), name='delete_booking'),
    path('app1/', RedirectView.as_view(pattern_name='app1:app1_create')),
    path('client_panel/', RedirectView.as_view(pattern_name='booking:create')),
    path('app2/', RedirectView.as_view(pattern_name='app2:app2_create')),
    path('change_status/<int:pk>/', tasks.change_status, name='change_status'),
    path('booking_delete/<int:pk>/', tasks.booking_delete, name='booking_delete')
]
