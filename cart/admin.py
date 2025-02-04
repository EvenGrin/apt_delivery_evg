from django.contrib import admin
from cart.models import Cart, Cabinet

@admin.register(Cart)
class CartView(admin.ModelAdmin):
    list_display = ('user', 'meal', 'quantity',)


@admin.register(Cabinet)
class CabView(admin.ModelAdmin):
    ordering = ('-num',)
    list_display = ('num', 'name',)
    search_fields = ('num', 'name__iregex')
    list_per_page = 10

