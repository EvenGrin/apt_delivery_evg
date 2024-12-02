from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):
    rules = forms.CharField(label='я согласен с правилами регистрации',
                            widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'last_name', 'first_name', 'patronymic')
