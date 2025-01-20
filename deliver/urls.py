from django.urls import path

from deliver import views

urlpatterns = [
    path('deliver/order_list', views.order_list, name="deliver"),
    path('deliver/<str:order>/<int:filter>', views.order_list, name="deliver"),
    path('deliver/take_order', views.take_order, name="take_order"),
    path('deliver/change_status_order', views.take_order, name="change_status_order"),
    path('deliver/order_history', views.take_order, name="order_history"),
]
