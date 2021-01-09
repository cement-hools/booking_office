from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from booking_office import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('api.urls')),
    path("auth/", include("django.contrib.auth.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
