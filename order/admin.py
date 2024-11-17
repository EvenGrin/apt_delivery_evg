from django.contrib import admin

from order.models import Order, Status, OrderMeal


class OrderAdmin(admin.ModelAdmin):
    list_display = ('date_create', 'user', 'status', 'amount')
    list_filter = ('status', )


admin.site.register(Order, OrderAdmin)
admin.site.register(Status)
admin.site.register(OrderMeal)
