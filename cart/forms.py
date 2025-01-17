from django.utils import timezone
from datetime import timedelta
from django import forms
from django.forms import DateTimeInput

from .models import User


class CreateOrderForm(forms.ModelForm):
    order_date = forms.DateTimeField(
        initial=lambda: (timezone.localtime() + timedelta(minutes=10)).strftime('%Y-%m-%dT%H:%M'),
        label='Дата и время получения заказа',
        widget=DateTimeInput(attrs={'type': 'datetime-local'})
    )

    def clean_order_date(self):
        order_date = self.cleaned_data['order_date']
        if order_date < timezone.now():
            raise forms.ValidationError("Дата и время не могут быть в прошлом")
        return order_date

    password = forms.CharField(
        label='Подтвердите паролем',
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ('order_date', 'password',)
