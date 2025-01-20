from django.contrib import admin

from order.models import Order, Status, OrderMeal


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('date_create', 'order_date', 'user', 'deliver', 'status', 'amount')
    list_filter = ('status', 'user',)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(OrderMeal)
class OrderMealView(admin.ModelAdmin):
    list_display = ('order', 'meal', 'amount',)
    list_filter = ('order',)
