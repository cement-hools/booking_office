from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (OfficeBookingViewSet, bookings_on_view, get_offices,
                    free_offices_view,
                    CreateUserView, BookingsViewSet)

all_booking = DefaultRouter()
office_booking_router = DefaultRouter()
registration_router = DefaultRouter()

office_booking_router.register('booking', OfficeBookingViewSet,
                               basename='booking')
all_booking.register('bookings', BookingsViewSet, basename='all_bookings')
registration_router.register('registration', CreateUserView, basename='reg')

urlpatterns = [
    path('', include(registration_router.urls)),  # регистрация пользователя
    path('', include(all_booking.urls)),
    # Вывести все рабочие места
    path('offices/', get_offices, name='get_offices'),
    path('office/<int:office_id>/', include(office_booking_router.urls),
         name='booking'),  # резервирование выбранного места
    path('offices/free', free_offices_view, name='free_offices'),
    # просмотр своюодныъ мест в диапозон времени

    path('v2/office/<int:office_id>/booking/', bookings_on_view,
         name='view_booking'),  # резервирование выбранного места через функцию

    path('auth/', include('rest_framework.urls'))

]
