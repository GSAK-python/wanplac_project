from django.urls import path

from app2 import tasks
from app2.views import BookingCreateView, App2BookingConfirmationView

app_name = 'app2'

urlpatterns = [
    path('create/', BookingCreateView.as_view(), name='app2_create'),
    path('confirm/', App2BookingConfirmationView.as_view(), name='confirm'),
]
