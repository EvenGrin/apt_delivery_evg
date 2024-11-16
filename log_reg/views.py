from lib2to3.fixes.fix_input import context

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from . import forms


def login_view(request: HttpRequest) -> HttpResponse:
    context = {}
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)

        if user is None:
            context = {
                'error': 'Неверный логин или пароль'
            }
            print('Все не правильно')
        else:
            login(request, user)
            return redirect('/')

    return render(request, 'log_reg/login.html', context)


def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        form = forms.RegisterForm()
        return render(request, 'log_reg/register.html', {
            'form': form
        })

    if request.method == "POST":
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')

        else:
            return render(request, 'log_reg/register.html', {
                'form': form
            })


def logout_view(request):
    logout(request)
    return redirect('/')