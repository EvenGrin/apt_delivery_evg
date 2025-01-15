from django import forms

from .models import User


class CreateOrderForm(forms.ModelForm):
    order_date = forms.SplitDateTimeField(label='Дата и время получения заказа')
    password = forms.CharField(label='Подтвердите паролем', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('password', )