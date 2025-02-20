from django.db import models


class Cabinet(models.Model):
    num = models.CharField(
        max_length=10,
        verbose_name="Номер"
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Название"
    )

    def __str__(self):
        return self.num

    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'
