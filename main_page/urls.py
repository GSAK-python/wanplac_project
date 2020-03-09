from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from main_page.views import MainPageView

app_name = 'main'

urlpatterns = [
    path('', MainPageView.as_view(), name='main'),
    path('app1/', RedirectView.as_view(pattern_name='app1:create2')),
    path('client_panel/', RedirectView.as_view(pattern_name='booking:create')),
    path('app2/', RedirectView.as_view(pattern_name='app2:app2_create'))
]
