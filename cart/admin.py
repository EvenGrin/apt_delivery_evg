from django.contrib import admin
from cart.models import Cart, Cabinet

@admin.register(Cart)
class CartView(admin.ModelAdmin):
    list_display = ('user', 'meal', 'quantity',)

@admin.register(Cabinet)
class CabView(admin.ModelAdmin):
    list_display = ('num', 'name',)


