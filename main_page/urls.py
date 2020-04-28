from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from main_page.views import MainPageView, BookingListView, ChooseDateView, BookingDetailView, AboutUsView, ContactView, \
    FAQView, RouteView, KayaksView, PriceListView, HowItLooksView, ProfileView

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
    path('app1/', RedirectView.as_view(pattern_name='app1:app1_create')),
    path('client_panel/', RedirectView.as_view(pattern_name='booking:create')),
    path('app2/', RedirectView.as_view(pattern_name='app2:app2_create'))
]
