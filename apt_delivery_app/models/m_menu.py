import datetime

from django.db import models

from apt_delivery_app.models import Meal


class Menu(models.Model):
    date = models.DateField(
        default=datetime.date.today() + datetime.timedelta(days=1),
        verbose_name='Дата',
        unique=True,
    )
    meal = models.ManyToManyField(
        Meal,
        verbose_name='Блюдо',
    )

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'
