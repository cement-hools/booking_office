from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Office, Booking
from api.serializers import BookingSerializer

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
        self.office_2 = Office.objects.create(info='#1')

        self.booking_1 = Booking.objects.create(
            date_from="2021-01-07T10:00Z",
            date_to="2021-01-07T12:00Z",
            tenant_name=self.user_1,
            tenant_info="первое",
            office=self.office_1
        )
        self.booking_2 = Booking.objects.create(
            date_from="2021-01-07T8:00Z",
            date_to="2021-01-07T9:00Z",
            tenant_name=self.user_1,
            tenant_info="second",
            office=self.office_1
        )

    def test_get(self):
        """Получаем список всех Booking."""
        url = reverse('get_booking', args=(self.booking_1.id,))
        # print('url:', url)
        bookings = Booking.objects.all()
        response = self.client.get(url)
        # print(response.data)
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
        url = reverse('get_booking', args=(self.booking_1.id,))
        self.client.force_login(self.user_1)
        response = self.client.post(url, data=data)
        # print(response.data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Booking.objects.all().count())
        new_booking = Booking.objects.all().last()
        serializer_data = BookingSerializer(new_booking).data

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(self.user_1.username,
                         new_booking.tenant_name.username)
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
        url = reverse('get_booking', args=(self.booking_1.id,))
        self.client.force_login(self.user_1)
        response = self.client.post(url, data=data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(2, Booking.objects.all().count())
