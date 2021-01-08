from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (BookingViewSet, get_booking, get_offices, training,
                    CreateUserView)

router = DefaultRouter()
registration_router = DefaultRouter()

router.register('booking', BookingViewSet, basename='booking')
registration_router.register('reg', CreateUserView, basename='reg')

urlpatterns = [
    path('', include(registration_router.urls)),
    path('booking/<int:office_id>/', get_booking, name='get_booking'),
    path('office/<int:office_id>/', include(router.urls)),
    path('tr', training, name='training'),
    path('', get_offices, name='get_offices'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
