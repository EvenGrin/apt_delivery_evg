from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name="Название"
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name