from django.db import models
from .meal import Meal
from .user import User


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    meal = models.ForeignKey(
        Meal,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="Блюдо"
    )
    quantity = models.IntegerField(
        default=None, verbose_name="Количество"
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    @property
    def total_quantity(self):
        return self.quantity

    @property
    def total_amount(self):
        return self.meal.price * self.quantity
