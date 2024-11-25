from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Meal(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название")
    price = models.FloatField(verbose_name="Цена")
    out = models.CharField(max_length=10, verbose_name="Выход")
    image = models.ImageField(upload_to='images', verbose_name="Изображение")
    category = models.ForeignKey(Category, default=None, on_delete=models.CASCADE,
                                 verbose_name="Категория")
    quantity = models.IntegerField(default=3, verbose_name="Количество")

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'


    def __str__(self):
        return self.name

