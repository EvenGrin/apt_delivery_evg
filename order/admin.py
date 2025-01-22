import datetime

from django.contrib import admin
from django.db.models import Q, Sum
from django.db.models.functions import TruncDay
from django.shortcuts import render
from django.urls import path
from django.utils import timezone

from home.models import Meal
from log_reg.models import User
from order.models import Order, Status, OrderMeal


class OrderMealInline(admin.TabularInline):
    model = OrderMeal
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('date_create', 'order_date', 'user', 'deliver', 'cab', 'status', 'result', 'amount', 'total_amount')
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

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sales_report/', self.admin_site.admin_view(self.sales_report_view), name='sales_report'),
            # path('users_report/', self.admin_site.admin_view(self.user_report_view), name='user_report'),
            # path('couriers_report/', self.admin_site.admin_view(self.courier_report_view), name='courier_report'),
            # path('frequency_report/', self.admin_site.admin_view(self.order_frequency_view), name='frequency_report'),
        ]
        return custom_urls + urls

    def sales_report_view(self, request):
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        start_date = None
        end_date = None

        if start_date_str and end_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').replace(tzinfo=timezone.utc)
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').replace(tzinfo=timezone.utc)
            except ValueError:
                pass

        orders = Order.objects.all()
        if start_date and end_date:
            orders = orders.filter(order_date__range=(start_date, end_date))

        # Суммарные продажи по дням
        sales_by_day = (
            orders.annotate(day=TruncDay('order_date'))
            .values('day')
            .annotate(total_sales=Sum('total_amount'))
            .order_by('day')
        )

        # Продажи по категориям
        sales_by_category = (
            Meal.objects.filter(order__in=orders)
            .values('category__name')
            .annotate(total_sales=Sum('price'))
            .order_by('-total_sales')
        )

        # Продажи по блюдам
        sales_by_dish = (
            Meal.objects.filter(order__in=orders)
            .values('name')
            .annotate(total_sales=Sum('price'))
            .order_by('-total_sales')
        )

        context = {
            'sales_by_day': sales_by_day,
            'sales_by_category': sales_by_category,
            'sales_by_dish': sales_by_dish,
            'title': 'Отчет по продажам'
        }
        return render(request, 'admin/sales_report.html', context)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    ordering = ('id',)


@admin.register(OrderMeal)
class OrderMealView(admin.ModelAdmin):
    list_display = ('order', 'meal', 'amount',)
    list_filter = ('order_id',)
