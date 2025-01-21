from django.urls import path

from deliver import views

urlpatterns = [
    path('deliver/deliver_orders/', views.deliver_orders, name="deliver_orders"),
    path('deliver/deliver_orders/<str:order>/<int:filter>', views.deliver_orders, name="deliver_orders"),
    path('deliver/order_list/', views.order_list, name="deliver"),
    path('deliver/order_list/<str:order>/<int:filter>', views.order_list, name="deliver"),
    path('deliver/take_order/', views.take_order, name="take_order"),
    path('deliver/update_status/', views.update_status, name="update_status")
]
