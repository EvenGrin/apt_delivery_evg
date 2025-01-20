from django.urls import path

from deliver import views

urlpatterns = [
    path('deliver/order_list/', views.order_list, name="deliver"),
    path('deliver/order_list/<str:order>/<int:filter>', views.order_list, name="deliver"),
    path('deliver/take_order/', views.take_order, name="take_order"),
    path('deliver/change_status_order/', views.change_status_order, name="change_status_order"),
    path('deliver/change_status_order/<str:order>/<int:filter>', views.change_status_order, name="change_status_order"),
    path('deliver/order_history/', views.order_history, name="order_history"),
    path('deliver/order_history/<str:order>/<int:filter>', views.order_history, name="order_history"),
]
