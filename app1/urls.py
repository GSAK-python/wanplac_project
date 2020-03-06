from django.urls import include, path
from app1.views import DailyBookingCreateView

app_name = 'app1'

urlpatterns = [
    path('create2/', DailyBookingCreateView.as_view(), name='create2'),
]