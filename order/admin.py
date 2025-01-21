from django.contrib import admin
from django.db.models import Q

from log_reg.models import User
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

    # def get_readonly_fields(self, request, obj=None):
    #     if request.user.is_superuser:
    #         return []
    #
    #     if request.user.groups.filter(name='deliver').exists():
    #         readonly_fields = ['user', 'cab', 'date_create', 'order_date', 'total_amount']
    #         if obj and obj.deliver and obj.deliver != request.user:
    #             readonly_fields.append('deliver')
    #         return readonly_fields
    #
    #     return self.readonly_fields
    #
    #
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     if request.user.groups.filter(name='deliver').exists():
    #         return qs.filter(Q(deliver=request.user) | Q(deliver=None)).exclude(cab=0)
    #     else:
    #         return qs
    #
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     """
    #     Ограничение списка курьеров
    #     """
    #     if db_field.name == 'deliver' and not request.user.is_superuser:
    #         kwargs['queryset'] = User.objects.filter(id=request.user.id)
    #         return db_field.formfield(**kwargs)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    ordering = ('id',)


@admin.register(OrderMeal)
class OrderMealView(admin.ModelAdmin):
    list_display = ('order', 'meal', 'amount',)
    list_filter = ('order_id',)
