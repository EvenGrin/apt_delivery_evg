from django.contrib import admin
from cart.models import Cart, Cabinet


class CartView(admin.ModelAdmin):
    list_display = ('user', 'meal', 'quantity',)


class CabView(admin.ModelAdmin):
    list_display = ('num', 'name',)


admin.site.register(Cart, CartView)
admin.site.register(Cabinet, CabView)
