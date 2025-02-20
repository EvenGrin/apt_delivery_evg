from datetime import timedelta, datetime

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import User


class RegisterForm(UserCreationForm):
    rules = forms.CharField(label='я согласен с правилами регистрации',
                            widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'patronymic', 'email', 'username',  'password1', 'password2',)

class CreateOrderForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user  # Сохраняем пользователя, чтобы получить его пароль

    # order_date = forms.DateTimeField(
    #     initial=lambda: (timezone.localtime() + timedelta(minutes=3)).strftime('%Y-%m-%d %H:%M'),
    #     label='Дата и время получения заказа',
    #     widget=DateTimeInput(attrs={'type': 'datetime-local'})
    # )
    # def clean_order_date(self):
    #     order_date = self.cleaned_data['order_date']
    #     if order_date < timezone.now():
    #         raise forms.ValidationError("Дата и время не могут быть в прошлом")
    #     return order_date
    user_comment = forms.CharField(
        widget=forms.Textarea,
        label='Комментарий к заказу',
        help_text='Не обязательное поле'
    )
    order_date = forms.DateField(
        initial=(timezone.localdate()).strftime('%Y-%m-%d'),
        label='Дата получения заказа',
        widget=forms.DateInput(attrs={'type': 'date', 'readonly': True}),  # Readonly, чтобы не меняли
    )
    order_time = forms.TimeField(
        initial=lambda: (timezone.localtime() + timedelta(minutes=3)).strftime('%H:%M'),
        label='Время получения заказа',
        widget=forms.TimeInput(attrs={'type': 'time'})
    )

    def clean(self):
        cleaned_data = super().clean()
        order_date = cleaned_data.get('order_date')
        order_time = cleaned_data.get('order_time')

        if order_date and order_time:
            if order_time < timezone.now().time():
                raise forms.ValidationError("Дата и время не могут быть в прошлом")
            else:
                cleaned_data['order_datetime'] = timezone.make_aware(datetime.combine(order_date, order_time))
        else:
            raise ValidationError("Введите и дату, и время.")

        return cleaned_data

    def clean_password(self):
        password = self.cleaned_data.get('password')
        user = self.user
        if user and not authenticate(username=user.username, password=password):
            raise forms.ValidationError("Неверный пароль")
        return password

    password = forms.CharField(
        label='Подтвердите паролем',
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ('order_date', 'order_time', 'password',)
