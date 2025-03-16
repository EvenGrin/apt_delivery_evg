from django.db import models
from django.utils import timezone

from .m_category import Category


class Meal(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Название"
    )
    price = models.IntegerField(
        verbose_name="Цена (руб.)"
    )
    out = models.CharField(
        max_length=10,
        verbose_name="Выход"
    )
    image = models.ImageField(
        upload_to='images',
        verbose_name="Изображение"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория",
        # related_name='meals',
    )
    quantity = models.IntegerField(
        default=3,
        verbose_name="Количество"
    )
    @property
    def in_menu(self):
        from .m_menu import Menu
        today = timezone.now().date()
        menus = Menu.objects.filter(date=today, meal=self)
        return menus.exists()

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return self.name


