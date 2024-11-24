from django.urls import path

from . import views

urlpatterns = [
    path('cart/', views.cart, name="cart"),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('sub-from-cart/', views.sub_from_cart, name='sub_from_cart'),
    path('cart_empty/', views.cart_empty, name='cart_empty'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
]
