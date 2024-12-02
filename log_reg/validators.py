from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible

@deconstructible
class LoginValidator(RegexValidator):
    regex = r"^[a-zA-Z0-9-]+\Z"
    message = 'Разрешенные символы (латиница, цифры и тире).'
    flags = 0

@deconstructible
class NameValidator(RegexValidator):
    regex = r"^[а-яА-Я -]+\Z"
    message = 'Разрешенные символы (кириллица, пробел и тире).'
    flags = 0