from django.urls import include, path
from app1.views import DailyBookingCreateView


booking_patterns = ([
                        path('create2/', DailyBookingCreateView.as_view(), name='create2')
                    ], 'booking')


urlpatterns = [
    path('booking/', include(booking_patterns)),
]