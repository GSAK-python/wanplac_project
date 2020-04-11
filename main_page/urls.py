from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from main_page.views import MainPageView, BookingListView, ChooseDateView, BookingDetailView

app_name = 'main'

urlpatterns = [
    path('', MainPageView.as_view(), name='main'),
    path('booking_confirmation/', BookingDetailView.as_view(), name='booking_detail'),
    path('my_booking/', BookingListView.as_view(), name='my_booking'),
    path('choose_date', ChooseDateView.as_view(), name='choose_date'),
    path('app1/', RedirectView.as_view(pattern_name='app1:app1_create')),
    path('client_panel/', RedirectView.as_view(pattern_name='booking:create')),
    path('app2/', RedirectView.as_view(pattern_name='app2:app2_create'))
]
