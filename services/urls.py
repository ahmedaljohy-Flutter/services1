from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('deliverys/', include('deliverys.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]