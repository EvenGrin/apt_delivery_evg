from django.urls import path

from . import views

urlpatterns = [
    path('order', views.order, name="order"),
    path('order/<str:order>/<int:filter>', views.order, name="order"),
]
