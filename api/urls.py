from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BookingViewSet, get_booking, get_offices, training

router = DefaultRouter()
router.register('booking', BookingViewSet,
                basename='booking')

urlpatterns = [
    path('booking/<int:office_id>/', get_booking, name='get_booking'),
    path('office/<int:office_id>/', include(router.urls)),
    path('tr', training, name='training'),
    path('', get_offices, name='get_offices'),
]
