from django.urls import path
from home import views

urlpatterns = [
    path('', views.meal_list, name="home"),

]
