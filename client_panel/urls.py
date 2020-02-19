from django.urls import path
from client_panel.views import BookingCreateView

app_name = 'booking'

urlpatterns = [
    path('create/', BookingCreateView.as_view(), name='create'),
]