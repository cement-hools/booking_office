from datetime import datetime

import dateutil.parser
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .models import Office, Booking
from .permissions import IsOwnerOrReadOnly, IsAdminUserOrReadOnly
from .serializers import (OfficeSerializer, BookingSerializer,
                          UserSerializer)

User = get_user_model()


class CreateUserView(mixins.CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUserOrReadOnly])
def get_offices(request):
    if request.method == 'GET':
        offices = Office.objects.all()
        serializer = OfficeSerializer(offices, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = OfficeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def bookings_on_view(request, office_id):
    if request.method == 'GET':
        office = get_object_or_404(Office, id=office_id)
        booking = office.booking.all()
        serializer = BookingSerializer(booking, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tenant_name=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfficeBookingViewSet(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    serializer_class = BookingSerializer

    def get_queryset(self):
        office_id = self.kwargs['office_id']
        office = get_object_or_404(Office.objects.prefetch_related('booking'),
                                   id=office_id)
        return office.booking.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BookingsViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        print(serializer.validated_data)
        serializer.save(owner=self.request.user)


@api_view(['GET'])
def free_offices_view(request):
    if request.method == 'GET':
        if request.GET:
            get_date_from = request.GET.get('datetime_from')
            get_date_to = request.GET.get('datetime_to')
            if get_date_from and get_date_to:
                get_date_from = get_date_from + '+00:00'
                get_date_to = get_date_to + '+00:00'
                date_format = '%Y-%m-%dT%H:%M%z'

                def getDateTimeFromISO8601String(s):
                    d = dateutil.parser.parse(s)
                    return d

                # a = getDateTimeFromISO8601String()
                # print(a)

                try:
                    # date_from = dateutil.parser.isoparse(get_date_from)
                    # date_to = dateutil.parser.isoparse(get_date_to)

                    date_from = datetime.strptime(get_date_from, date_format)
                    date_to = datetime.strptime(get_date_to, date_format)
                except Exception as exc:
                    print('---except---', exc)
                    return Response({'error GET': ('формат ввода '
                                                   'datetime_from=2021-01-08T13:00&'
                                                   'datetime_to=2021-01-08T15:00')})

                free_offices = Office.objects.prefetch_related(
                    'booking').exclude(
                    Q(booking__date_from__range=(date_from, date_to)) | Q(
                        booking__date_to__range=(date_to, date_to))
                ).exclude(
                    booking__date_from__lte=date_from,
                    booking__date_to__gte=date_to
                ).exclude(
                    booking__date_from__lte=date_to,
                    booking__date_to__gte=date_from
                )
                serializer = OfficeSerializer(free_offices, many=True)
                return Response(serializer.data)
        return Response({'error GET': ('формат ввода '
                                       'datetime_from=2021-01-08T13:00Z&'
                                       'datetime_to=2021-01-08T15:00Z')})
