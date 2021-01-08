from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Office, Booking
from .serializers import OfficeSerializer, BookingSerializer, \
    TrainingSerializer


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
        # print(request.data)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BookingSerializer(data=request.data)
        # print(request.data)
        # apts_booked1 = Booking.objects.filter(Q(date_from__range=(query_start, query_end)) | Q(date_to__range=(query_start, query_end)
        if serializer.is_valid():
            # date_from = serializer.validated_data['date_from']
            # date_to = serializer.validated_data['date_to']
            # booked1 = Booking.objects.filter(
            #     Q(date_from__range=(date_from, date_to)) | Q(
            #         date_to__range=(date_to, date_to)))
            # booked2 = Booking.objects.filter(
            #     date_from__lte=date_from).filter(date_to__gte=date_to)
            # booked = booked1.exists() | booked2.exists()
            # if booked:
            #     print('занято')
            #     raise serializers.ValidationError(
            #         code=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
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
    # apts_booked1 = Rental.objects.values_list('id', flat=True).select_related().filter(
    # Q(booking__arrival_date__range=(query_start, query_end)) | Q(booking__departure_date__range=(query_start, query_end))
    # ).distinct('id')
    # apts_booked2 = Rental.objects.values_list('id', flat=True).select_related().filter(
    # booking__arrival_date__lte=query_start).filter(booking__departure_date__gte=query_end).distinct('id')
    # apts_booked = apts_booked1 | apts_booked2
    if request.method == 'GET':
        booking = Booking.objects.all()
        first = booking[0]
        print(first.date_from.day)
        serializer = TrainingSerializer(booking, many=True)
        return Response(serializer.data)
