from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, Sum
from django.urls import reverse
from django.utils import timezone

from .m_cabinet import Cabinet
from .m_user import User


def get_default_created_at():
    # print(timezone.now(), 'с модели')
    return timezone.localtime() + timedelta(minutes=3)


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    date_create = models.DateTimeField(
        verbose_name='Дата заказа',
        auto_now_add=True
    )
    order_date = models.TimeField(
        default=get_default_created_at,
        verbose_name='Дата и время получения заказа'
    )
    status = models.ForeignKey(
        'Status',
        on_delete=models.CASCADE,
        verbose_name='Статус',
        default=1
    )
    result = models.CharField(
        max_length=50,
        verbose_name='Причина отказа',
        blank=True, null=True
    )
    user_comment = models.TextField(
        blank=True,
        null=True,
        verbose_name='Комментарий пользователя к заказу',

        help_text='Не обязательное поле'
    )
    cab = models.ForeignKey(
        Cabinet,
        on_delete=models.CASCADE,
        verbose_name='Кабинет',
        default=1
    )
    deliver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='courier_orders',
        blank=True,
        null=True,
        limit_choices_to={'groups__name': 'deliver'},
        verbose_name="Курьер"
    )

    @property
    def total_amount(self):
        total = 0
        for item in self.ordermeal_set.all():  # ordermeal_set - обратный related_name
            total += item.meal.price * item.amount
        return total

    total_amount.fget.short_description = 'Сумма заказа'

    @property
    def amount(self):
        return self.ordermeal_set.filter(order=self.pk).aggregate(Sum('amount'))['amount__sum']

    amount.fget.short_description = 'Количество'

    @property
    def meals(self):
        return self.ordermeal_set.filter(order=self.pk)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def clean(self):
        if self.status.id == 3 and not self.result:
            raise ValidationError({'result': 'Обязательное поле при статусе "Отменён"'})
        # if self.status.id > 3 and self.deliver is None:
        #     raise ValidationError({'deliver': 'Укажите курьера'})
        if self.cab.id == 0 and self.deliver:
            raise ValidationError({'deliver': 'К самовыносу курьер не указывается'})

    def get_absolute_url(self):  # Тут мы создали новый метод
        return reverse('order')

    def __str__(self):
        return f'№: {self.id},\n покупатель: {self.user},\n дата: {str(self.date_create).split(".")[0]}'
