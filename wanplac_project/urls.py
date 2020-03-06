from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('client_panel/', include('client_panel.urls')),
    path('app1/', include('app1.urls', namespace='app1')),
    path('main/', include('main_page.urls', namespace='main'))
]
