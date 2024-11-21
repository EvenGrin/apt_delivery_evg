from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

from home.models import Meal


# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, default=None, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=None)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    @property
    def total_quantity(self):
        return self.quantity

    @property
    def total_amount(self):
        return self.meal.price * self.quantity



class Cabinet(models.Model):
    num = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.num

    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'
