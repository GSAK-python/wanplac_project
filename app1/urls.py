from django.urls import include, path
from app1.views import BookingCreateView

app_name = 'app1'

urlpatterns = [
    path('create/', BookingCreateView.as_view(), name='app1_create'),
]