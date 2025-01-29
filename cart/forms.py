from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from django import forms
from django.forms import DateTimeInput

from .models import User


class CreateOrderForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user  # Сохраняем пользователя, чтобы получить его пароль

    order_date = forms.DateTimeField(
        initial=lambda: (timezone.localtime() + timedelta(minutes=3)).strftime('%Y-%m-%d %H:%M'),
        label='Дата и время получения заказа',
        widget=DateTimeInput(attrs={'type': 'datetime-local'})
    )
    def clean_order_date(self):
        order_date = self.cleaned_data['order_date']
        if order_date < timezone.now():
            raise forms.ValidationError("Дата и время не могут быть в прошлом")
        return order_date

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
        fields = ('order_date', 'password',)
