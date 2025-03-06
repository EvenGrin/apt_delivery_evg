from datetime import timedelta, time

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import User, Order, Meal, OrderMeal


class RegisterForm(UserCreationForm):
    rules = forms.CharField(label='я согласен с правилами регистрации',
                            widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'patronymic', 'email', 'username',  'password1', 'password2',)

class CreateOrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    user_comment = forms.CharField(
        widget=forms.Textarea,
        label='Комментарий к заказу',
        help_text='Не обязательное поле',
        required = False
    )
    order_date = forms.TimeField(
        initial=lambda: (timezone.localtime() + timedelta(minutes=3)).strftime('%H:%M'),
        label='Время получения заказа',
        widget=forms.TimeInput(attrs={'type': 'time'}),
        help_text='Время указывается не раньше текущей'
    )

    def clean(self):
        cleaned_data = super().clean()
        order_date = cleaned_data.get('order_date')
        print(order_date, timezone.localtime().time())
        if order_date:
            # print(time(8, 00) < order_date < time(15, 00))
            if order_date < timezone.localtime().time():
                raise forms.ValidationError("Время не могут быть в прошлом")
            else:
                cleaned_data['order_date'] = order_date
        else:
            raise ValidationError("Введите время.")

        return cleaned_data


    class Meta:
        model = Order
        fields = ()


class ChangeOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('cab', 'user_comment', 'order_date',)


class ChangeOrderMealForm(forms.ModelForm):
    class Meta:
        model = OrderMeal
        fields = '__all__'