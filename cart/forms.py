from django import forms

from .models import User


class CreateOrderForm(forms.ModelForm):
    password = forms.CharField(label='Подтвердите паролем', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('password', )