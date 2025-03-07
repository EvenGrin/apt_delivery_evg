from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=30, null=True)
    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return self.name