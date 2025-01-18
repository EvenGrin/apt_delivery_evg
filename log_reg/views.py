from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from . import forms


# def login_view(request: HttpRequest) -> HttpResponse:
#     context = {}
#     if request.method == 'POST':
#         username = request.POST["username"]
#         password = request.POST["password"]
#         user = authenticate(username=username, password=password)
#
#         if user is None:
#             context = {
#                 'error': 'Неверный логин или пароль'
#             }
#             print('Все не правильно')
#         else:
#             login(request, user)
#             return redirect('/')
#
#     return render(request, 'log_reg/login.html', context)


def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('login')
    else:
        form = forms.RegisterForm()
    return render(request, 'registration/registration.html', {
        'form': form
    })


def logout_view(request):
    logout(request)
    return redirect('/')
