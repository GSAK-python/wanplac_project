from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView
from django.urls import path, include
from client_panel.views import BookingCreateView

booking_patterns = ([
                        path('create/', BookingCreateView.as_view(), name='create'),
                    ], 'booking')

registration_patterns = ([
                             path('login/', LoginView.as_view(), name='login'),
                             path('logout/', LogoutView.as_view(), name='logout'),
                             path('password_reset/',
                                  PasswordResetView.as_view(
                                      template_name='registration/password_reset_form.html',
                                      subject_template_name='registration/password_reset_subject.txt',
                                      email_template_name='registration/password_reset_email.html',
                                      success_url='registration/login/'),
                                  name='password_reset'),
                             path('password_reset_done/',
                                  PasswordResetDoneView.as_view(
                                      template_name='registration/password_reset_done.html'
                                  ),
                                  name='password_reset_done'),
                         ], 'registration')

urlpatterns = [
    path('booking/', include(booking_patterns)),
    path('registration/', include(registration_patterns)),
]
