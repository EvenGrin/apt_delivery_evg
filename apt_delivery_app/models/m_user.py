from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import LoginValidator, NameValidator


class User(AbstractUser):
    username = (
        models.CharField(
            'Логин',
            max_length=150,
            unique=True,
            help_text="Обязательное поле. Только латиница, цифры и тире.",
            validators=[LoginValidator()],
            error_messages={"unique": _("Пользователь с таким именем уже существует"), })
    )
    first_name = models.CharField(
        _("first name"),
        max_length=150,
        validators=[NameValidator()]
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
        validators=[NameValidator()]
    )
    patronymic = models.CharField(
        'Отчество',
        max_length=150,
        blank=True,
        validators=[NameValidator()]
    )

    def is_deliver(self):
        return self.groups.filter(name='deliver').exists()

    def is_operator(self):
        return self.groups.filter(name='operator').exists()

    def __str__(self):
        return "%s %s %s" % (self.last_name, self.first_name, self.patronymic,)
