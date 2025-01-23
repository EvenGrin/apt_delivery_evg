from django.urls import path
from setuptools.extern import names

from home import views

urlpatterns = [
    path('', views.meal_list, name="home"),

]
