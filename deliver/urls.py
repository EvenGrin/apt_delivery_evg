from django.urls import path

from deliver import views

urlpatterns = [
    path('deliver/', views.deliver_order_list, name="deliver"),
    path('deliver/<str:order>/<int:filter>', views.deliver_order_list, name="deliver"),
    path('deliver/take_order', views.take_order, name="take_order"),
]
