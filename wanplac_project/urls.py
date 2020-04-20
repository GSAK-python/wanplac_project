from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from wanplac_project import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('client_panel/', include('client_panel.urls')),
    path('app1/', include('app1.urls', namespace='app1')),
    path('app2/', include('app2.urls', namespace='app2')),
    path('main/', include('main_page.urls', namespace='main'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
