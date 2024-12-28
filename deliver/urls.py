from django.urls import path

from deliver import views

urlpatterns = [
    path('deliver/', views.deliver_order_list , name="deliver"),
]