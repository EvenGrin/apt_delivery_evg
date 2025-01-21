from django.contrib import admin
from django.db.models import Q

from order.models import Order, Status, OrderMeal


class OrderMealInline(admin.TabularInline):
    model = OrderMeal
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('date_create', 'order_date', 'user', 'deliver', 'cab', 'status', 'result', 'amount')
    list_filter = ('status', 'date_create', 'order_date', 'user', 'deliver', 'cab')
    list_editable = ('deliver', 'status')
    inlines = [OrderMealInline]
    list_per_page = 10

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='deliver').exists():
            return qs.filter(Q(deliver=request.user) | Q(deliver=None)).exclude(cab=0)
        else:
            return qs


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    ordering = ('id',)


@admin.register(OrderMeal)
class OrderMealView(admin.ModelAdmin):
    list_display = ('order', 'meal', 'amount',)
    list_filter = ('order_id',)
