from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Office(models.Model):
    info = models.CharField(verbose_name='Инфо о Помещении', max_length=10000,
                            null=True)

    def __str__(self):
        return f'Помещение № {self.id}'

    class Meta:
        verbose_name_plural = 'Помещения'
        verbose_name = 'Помещение'


class Booking(models.Model):
    date_from = models.DateTimeField(verbose_name='Дата начала бронирования', )
    date_to = models.DateTimeField(verbose_name='Дата окончание бронирования')
    owner = models.ForeignKey(User, verbose_name='Бронирующий',
                              related_name='booking',
                              on_delete=models.CASCADE, )
    tenant_info = models.CharField(verbose_name='Инфо о бронировании',
                                   max_length=10000)
    office = models.ForeignKey(Office, verbose_name='Помещение',
                               related_name='booking',
                               on_delete=models.CASCADE, )

    def __str__(self):
        return f'Помещение №{self.office.id}: Бронь №{self.id}'

    class Meta:
        verbose_name_plural = 'Бронь'
        verbose_name = 'Бронь'
