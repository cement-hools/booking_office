from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Office, Booking
from .serializers import BookingSerializer, UserSerializer

User = get_user_model()


class BookingApiTestCase(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create(username='test_username_1',
                                          email='test1@mail.ru', )
        self.user_staff = User.objects.create(
            username='test_username_staff',
            email='test@mail.ru',
            is_staff=True,
        )

        self.office_1 = Office.objects.create(info='#1')
        self.office_2 = Office.objects.create(info='#2')

        self.booking_1 = Booking.objects.create(
            date_from="2021-01-07T10:00Z",
            date_to="2021-01-07T12:00Z",
            owner=self.user_1,
            tenant_info="первое",
            office=self.office_1
        )
        self.booking_2 = Booking.objects.create(
            date_from="2021-01-07T8:00Z",
            date_to="2021-01-07T9:00Z",
            owner=self.user_1,
            tenant_info="second",
            office=self.office_1
        )

    def test_registration(self):
        """Создание нового пользователя."""
        self.assertEqual(2, User.objects.all().count())

        data = {
            'username': 'terminator',
            'password': 'qwerty'
        }

        url = reverse('reg-list')
        response = self.client.post(url, data=data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, User.objects.all().count())

        new_user = User.objects.all().last()
        serializer_data = UserSerializer(new_user).data

        self.assertEqual(response.data, serializer_data)
        self.assertEqual('terminator', new_user.username)

    def test_get(self):
        """Получаем список всех Booking."""
        url = reverse('booking-list', args=(self.booking_1.id,))
        bookings = Booking.objects.all()
        response = self.client.get(url)
        serializer_data = BookingSerializer(bookings, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        """Создание нового Booking."""
        self.assertEqual(2, Booking.objects.all().count())
        data = {
            "date_from": "2021-01-09T10:00:00Z",
            "date_to": "2021-01-09T12:00:00Z",
            "tenant_info": "на сутки",
            "office": 1
        }
        url = reverse('booking-list', args=(self.booking_1.id,))
        self.client.force_login(self.user_1)
        response = self.client.post(url, data=data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Booking.objects.all().count())
        new_booking = Booking.objects.all().last()
        serializer_data = BookingSerializer(new_booking).data

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(self.user_1.username,
                         new_booking.owner.username)
        self.assertEqual(1, new_booking.office.id)

    def test_create_on_the_booked_date(self):
        """Создание нового Booking на занятую дату."""
        self.assertEqual(2, Booking.objects.all().count())
        data = {
            "date_from": "2021-01-07T11:00Z",
            "date_to": "2021-01-07T13:00Z",
            "tenant_info": "на забронированую",
            "office": 1
        }
        url = reverse('booking-list', args=(self.booking_1.id,))
        self.client.force_login(self.user_1)
        response = self.client.post(url, data=data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(2, Booking.objects.all().count())

    def test_create_on_the_booked_date_2(self):
        """Создание нового Booking на занятую дату."""
        self.assertEqual(2, Booking.objects.all().count())
        data = {
            "date_from": "2021-01-07T11:00Z",
            "date_to": "2021-01-07T13:00Z",
            "tenant_info": "на забронированую",
            "office": 2
        }
        url = reverse('booking-list', args=(self.booking_1.id,))
        self.client.force_login(self.user_1)
        response = self.client.post(url, data=data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Booking.objects.all().count())

    def test_free_offices_on_free_date(self):
        """Вывод мест в незанятую дату"""
        url = reverse('free_offices')
        date_from = "2021-03-07T21:00"
        date_to = "2021-03-07T23:00"
        get_url = f"{url}?datetime_from={date_from}&datetime_to={date_to}"

        self.client.force_login(self.user_1)
        response = self.client.get(get_url)

        self.assertEqual(2, len(response.data))

    def test_free_offices_on_booking_date(self):
        """Вывод мест в незанятую дату и одно место входит в диапозон"""
        date_from = "2021-01-07T10:00"
        date_to = "2021-01-07T13:00"
        url = reverse('free_offices')
        get_url = f"{url}?datetime_from={date_from}&datetime_to={date_to}"

        self.client.force_login(self.user_1)
        response = self.client.get(get_url)
        self.assertEqual('#2', response.data[0].get('info'))
