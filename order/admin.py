import json
from datetime import datetime, timezone

from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Count, OuterRef, Subquery, Value, Max, Min
from django.db.models.functions import TruncDay, Concat, Greatest
from django.shortcuts import render
from django.urls import path, reverse
from django.utils import timezone

from home.models import Meal
from order.models import Order, Status, OrderMeal


class OrderMealInline(admin.TabularInline):
    model = OrderMeal
    extra = 0
    readonly_fields = [field.name for field in OrderMeal._meta.get_fields()]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'date_create', 'order_date', 'user', 'deliver', 'cab', 'status', 'result', 'amount', 'total_amount')
    list_filter = ('status', 'date_create', 'order_date', 'user', 'deliver', 'cab')
    list_editable = ('deliver', 'status', 'result')
    inlines = [OrderMealInline]
    search_fields = ('id__iexact',)
    list_per_page = 10

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []

        if request.user.groups.filter(name='operator').exists():
            readonly_fields = ['user', 'cab', 'date_create', 'order_date', 'total_amount']
            return readonly_fields

        return self.readonly_fields

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sales_report/', self.admin_site.admin_view(self.sales_report_view), name='sales_report'),
            path('users_report/', self.admin_site.admin_view(self.user_report_view), name='user_report'),
            path('couriers_report/', self.admin_site.admin_view(self.courier_report_view), name='courier_report'),
        ]
        return custom_urls + urls

    def get_app_links(self, request):
        app_list = admin.site.get_app_list(request)
        links = []
        for app in app_list:
            app_label = app['app_label']
            links.append({'url': reverse('admin:app_list', kwargs={'app_label': app_label}), 'label': app['name']})
        return links

    def get_admin_links(self, obj=None):
        links = []
        links.append({'url': reverse('admin:sales_report'), 'label': 'Отчет по продажам'})
        links.append({'url': reverse('admin:user_report'), 'label': 'Отчет по пользователям'})
        links.append({'url': reverse('admin:courier_report'), 'label': 'Отчет по курьерам'})
        return links

    def changelist_view(self, request, extra_context=None):
        if not extra_context:
            extra_context = {}
        extra_context['custom_links'] = self.get_admin_links()
        extra_context['app_links'] = self.get_app_links(request)
        return super().changelist_view(request, extra_context=extra_context)

    # отчет по продажам
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

        subquery = OrderMeal.objects.filter(order=OuterRef('pk')).annotate(
            total_price=ExpressionWrapper(F('meal__price') * F('amount'), output_field=DecimalField())
        ).values('order').annotate(total_amount=Sum('total_price')).values('total_amount')

        # Суммарные продажи по дням
        sales_by_day = orders.annotate(
            date=TruncDay('order_date'),
            total_amount=Subquery(subquery),
        ).values('date').annotate(total_sales=Sum('total_amount')).order_by('date')

        # Продажи по категориям
        meal_ids = OrderMeal.objects.filter(order__in=orders).values_list('meal_id', flat=True)

        # 2. Сгруппируем meals по категории и посчитаем total_sales
        sales_by_category = (
            Meal.objects.filter(id__in=meal_ids)
            .values('category__name')
            .annotate(total_sales=Sum('price'))
            .order_by('-total_sales')
        )

        # Продажи по блюдам
        sales_by_dish = (
            Meal.objects.filter(id__in=meal_ids)
            .values('name', 'category__name')
            .annotate(total_sales=Sum('price'))
            .order_by('-total_sales')
        )
        context = {
            'sales_by_day': json.dumps(list(sales_by_day), default=str),
            'sales_by_category': json.dumps(list(sales_by_category)),
            'sales_by_dish': json.dumps(list(sales_by_dish)), 'title': 'Отчет по продажам',
            'custom_links': self.get_admin_links(),
            'app_links': self.get_app_links(request),
            'start_date': start_date if start_date else orders.aggregate(date=Min('order_date'))['date'],
            'end_date': end_date if end_date else orders.aggregate(date=Max('order_date'))['date'],
            **admin.site.each_context(request)
        }
        return render(request, 'admin/sales_report.html', context)

    def user_report_view(self, request):
        user_type = request.GET.get('user_type', 'all')  # Default to 'all'
        all_clients = Order.objects.values('user__id').distinct().annotate(
            user__username=Concat(
                'user__last_name', Value(' '),
                'user__first_name', Value(' '),
                'user__patronymic'
            ),
            count=Count('user'))
        user_data = {
            'clients': list(all_clients.order_by('-count')),
        }
        # print(user_data)

        context = {
            'user_data': user_data,
            'user_type': user_type,
            'title': 'Отчет по пользователям',
            'custom_links': self.get_admin_links(),
            'app_links': self.get_app_links(request),
            **admin.site.each_context(request)
        }
        return render(request, 'admin/user_report.html', context)

    def courier_report_view(self, request):
        subquery = OrderMeal.objects.filter(order=OuterRef('pk')).annotate(
            total_price=ExpressionWrapper(F('meal__price') * F('amount'), output_field=DecimalField())
        ).values('order').annotate(total_amount=Sum('total_price')).values('total_amount')

        couriers = (
            Order.objects.filter(deliver__isnull=False)
            .values('deliver')
            .annotate(
                deliver__username=Concat(
                    'deliver__last_name', Value(' '),
                    'deliver__first_name', Value(' '),
                    'deliver__patronymic'
                ),
                count=Count('deliver'),
            )
            .order_by('-count')
        )

        context = {
            'couriers': list(couriers),
            'title': 'Отчет по курьерам',
            'custom_links': self.get_admin_links(),
            'app_links': self.get_app_links(request),
            **admin.site.each_context(request)
        }
        return render(request, 'admin/courier_report.html', context)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    ordering = ('id',)


@admin.register(OrderMeal)
class OrderMealView(admin.ModelAdmin):
    list_display = ('order_id', 'order', 'meal', 'amount',)
    list_filter = ('order_id',)
    search_fields = ('order_id__id__iexact',)
    list_per_page = 10