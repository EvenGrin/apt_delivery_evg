from django.urls import path, include
from . import views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path('accounts/registration', views.register_view, name='registration'),
    path('logout/', views.logout_view, name='logout'),
]
