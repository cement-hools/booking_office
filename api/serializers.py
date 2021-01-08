from django.db.models import Q
from rest_framework import serializers, status

from .models import Office, Booking


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Office


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Booking

    def create(self, validated_data):
        date_from = validated_data['date_from']
        date_to = validated_data['date_to']
        booked1 = Booking.objects.filter(
            Q(date_from__range=(date_from, date_to)) | Q(
                date_to__range=(date_to, date_to)))
        booked2 = Booking.objects.filter(
            date_from__lte=date_from).filter(date_to__gte=date_to)
        booked = booked1.exists() | booked2.exists()
        if booked:
            print('занято')
            raise serializers.ValidationError(
                code=status.HTTP_400_BAD_REQUEST)
        return Booking.objects.create(**validated_data)


class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('date_from', 'date_to',)
        model = Booking
