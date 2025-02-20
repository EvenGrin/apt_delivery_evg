from django.contrib.auth import login, logout
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from apt_delivery_app import forms


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