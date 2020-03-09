from django.urls import path

from app2.views import BookingCreateView

app_name = 'app2'

urlpatterns = [
    path('create/', BookingCreateView.as_view(), name='app2_create'),
]