from django.urls import path
from setuptools.extern import names

from home import views

urlpatterns = [
    path('', views.meal_list, name="home"),
    path('menu/', views.menu, name="menu"),
    path('ajax/', views.meal_list_ajax, name="home_ajax")
]
