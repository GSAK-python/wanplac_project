from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView, LogoutView
from django.urls import path, include, reverse_lazy
from client_panel.views import BookingCreateView, SignUpCreateView, Login, CPBookingConfirmationView

booking_patterns = ([
                        path('create/', BookingCreateView.as_view(), name='create'),
                        path('confirm/', CPBookingConfirmationView.as_view(), name='confirm'),
                    ], 'booking')


registration_patterns = ([
                             path('login/', Login.as_view(), name='login'),
                             path('logout/', LogoutView.as_view(), name='logout'),
                             path('password_reset/', PasswordResetView.as_view(
                                 success_url=reverse_lazy('registration:password_reset_done')), name='password_reset'),
                             path('password_reset_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
                             path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
                                 success_url=reverse_lazy('registration:password_reset_complete')),
                                  name='password_reset_confirm'),
                             path('password_reset_complete/', PasswordResetCompleteView.as_view(),
                                  name='password_reset_complete'),
                             path('sign_up/', SignUpCreateView.as_view(success_url=reverse_lazy('registration:login')),
                                  name='sign_up')
                         ], 'registration')

urlpatterns = [
    path('booking/', include(booking_patterns, namespace='booking')),
    path('registration/', include(registration_patterns, namespace='registration')),
]
