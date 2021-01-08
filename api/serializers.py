from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers, status
from rest_framework.serializers import ModelSerializer

from .models import Office, Booking

User = get_user_model()


class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class OfficeSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Office


class BookingSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Booking

    tenant_name = serializers.SlugRelatedField(slug_field='username',
                                               read_only=True)

    def create(self, validated_data):
        date_from = validated_data['date_from']
        date_to = validated_data['date_to']
        booked_1 = Booking.objects.filter(
            Q(date_from__range=(date_from, date_to)) | Q(
                date_to__range=(date_to, date_to)))
        booked_2 = Booking.objects.filter(
            date_from__lte=date_from).filter(date_to__gte=date_to)
        booked_3 = Booking.objects.filter(date_from__lte=date_to,
                                          date_to__gte=date_from)

        booked = booked_1.exists() | booked_2.exists() | booked_3.exists()
        if booked:
            print('занято')
            raise serializers.ValidationError(
                code=status.HTTP_400_BAD_REQUEST)
        return Booking.objects.create(**validated_data)


class TrainingSerializer(ModelSerializer):
    class Meta:
        fields = ('date_from', 'date_to',)
        model = Booking
