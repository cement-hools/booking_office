from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Office, Booking
from .serializers import (OfficeSerializer, BookingSerializer,
                          TrainingSerializer, UserSerializer)

User = get_user_model()


class CreateUserView(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


@api_view(['GET', 'POST'])
def get_offices(request):
    if request.method == 'GET':
        offices = Office.objects.all()
        serializer = OfficeSerializer(offices, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def get_booking(request, office_id):
    if request.method == 'GET':
        office = get_object_or_404(Office, id=office_id)
        booking = office.booking.all()
        serializer = BookingSerializer(booking, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            if request.user.is_authenticated:
                serializer.save(tenant_name=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BookingViewSet(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = BookingSerializer

    def get_queryset(self):
        office_id = self.kwargs['office_id']
        office = get_object_or_404(Office, id=office_id)
        return office.booking.all()

    # def perform_create(self, serializer):
    #     title_id = self.kwargs['title_id']
    #     title = get_object_or_404(Title, id=title_id)
    #     serializer.save(author=self.request.user, title=title)


@api_view(['GET', 'POST'])
def training(request):
    if request.method == 'GET':
        booking = Booking.objects.all()
        first = booking[0]
        print(first.date_from.day)
        serializer = TrainingSerializer(booking, many=True)
        return Response(serializer.data)
