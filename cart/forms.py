from django.utils import timezone
from datetime import datetime, date, timedelta
from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateTimeInput

from .models import User


class CreateOrderForm(forms.ModelForm):
    order_date = forms.SplitDateTimeField(
        initial=lambda: (timezone.localtime()+timedelta(minutes=10)).strftime('%Y-%m-%dT%H:%M'),
        input_date_formats=['%Y-%m-%d %H:%M'],
        label='Дата и время получения заказа',
        widget=DateTimeInput(attrs={'type': 'datetime-local'})
    )

    def clean_order_date(self):
        order_date = self.cleaned_data['order_date']
        if order_date.date() < timezone.now().date():
            self.add_error('order_date',"Дата и время не могут быть в прошлом")
        return order_date



    password = forms.CharField(
        label='Подтвердите паролем',
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ('order_date','password',)
