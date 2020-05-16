from django.urls import path

from app2 import tasks
from app2.views import BookingCreateView, App2BookingConfirmationView

app_name = 'app2'

urlpatterns = [
    path('create/', BookingCreateView.as_view(), name='app2_create'),
    path('confirm/', App2BookingConfirmationView.as_view(), name='confirm'),
    path('change_status/<int:pk>/', tasks.change_status, name='change_status'),
    path('booking_delete/<int:pk>/', tasks.booking_delete, name='booking_delete')
]
