from symtable import Class

from django.db import models

class DayOfWeek(models.Model):
    name = models.CharField(max_length=15, unique=True, verbose_name="День недели")  # 'Понедельник', 'Вторник' и т.д.
    class Meta:
        verbose_name = 'День недели'
        verbose_name_plural = 'Дни недели'
    def __str__(self):
        return self.name

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
                                 verbose_name="Категория", related_name='meals')
    quantity = models.IntegerField(default=3, verbose_name="Количество")
    days = models.ManyToManyField(DayOfWeek, blank=True)
    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'


    def __str__(self):
        return self.name



class Menu(models.Model):
    days = models.ManyToManyField(DayOfWeek, blank=True)
    meal = models.OneToOneField(Meal, default=None, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'
    def __str__(self):
        return self.meal.name
