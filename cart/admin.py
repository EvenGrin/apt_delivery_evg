from django.contrib import admin
from cart.models import Cart


class CartView(admin.ModelAdmin):
    list_display = ('user', 'meal', 'quantity',)


admin.site.register(Cart, CartView)