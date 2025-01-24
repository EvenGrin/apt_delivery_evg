import json
from django.contrib import admin
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Count, OuterRef, Subquery, Value
from django.db.models.functions import TruncDay, Concat
from django.shortcuts import render
from django.urls import path, reverse
from django.utils import timezone
from datetime import datetime, timezone
from home.models import Meal
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
            path('users_report/', self.admin_site.admin_view(self.user_report_view), name='user_report'),
            path('couriers_report/', self.admin_site.admin_view(self.courier_report_view), name='courier_report'),
            path('frequency_report/', self.admin_site.admin_view(self.order_frequency_view), name='frequency_report'),
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
        links.append({'url': reverse('admin:frequency_report'), 'label': 'Отчет по частоте заказов'})
        return links

    def changelist_view(self, request, extra_context=None):
        if not extra_context:
            extra_context = {}
        extra_context['custom_links'] = self.get_admin_links()
        extra_context['app_links'] = self.get_app_links(request)
        return super().changelist_view(request, extra_context=extra_context)

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
            'app_links': self.get_app_links(request)
        }
        return render(request, 'admin/sales_report.html', context)

    def user_report_view(self, request):
        user_type = request.GET.get('user_type', 'all')  # Default to 'all'
        all_clients = Order.objects.values('user__id').distinct().annotate(
            user__username=Concat(
                'user__first_name', Value(' '),
                'user__last_name', Value(' '),
                'user__patronymic'
            ),
            count=Count('user'))
        all_couriers = Order.objects.filter(deliver__isnull=False).values('deliver__id').distinct().annotate(
            deliver__username=Concat(
                'deliver__first_name', Value(' '),
                'deliver__last_name', Value(' '),
                'deliver__patronymic'
            ),
            count=Count('deliver'))
        user_data = {
            'clients': list(all_clients.order_by('-count')),
            'couriers': list(all_couriers.order_by('-count')),
        }
        print(user_data)

        context = {
            'user_data': user_data,
            'user_type': user_type,
            'title': 'Отчет по пользователям',
            'custom_links': self.get_admin_links(),
            'app_links': self.get_app_links(request)
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
                order_count=Count('deliver'),
                avg_amount=Sum(Subquery(subquery)) / Count('deliver'),
            )
            .order_by('-order_count')
        )

        context = {
            'couriers': couriers,
            'title': 'Отчет по курьерам',
            'custom_links': self.get_admin_links(),
            'app_links': self.get_app_links(request)}
        return render(request, 'admin/courier_report.html', context)

    def order_frequency_view(self, request):
        frequency = (
            Order.objects.values('user')
            .annotate(order_count=Count('user'))
            .order_by('-order_count')
        )
        context = {
            'frequency': frequency,
            'title': 'Анализ частоты заказов',
            'custom_links': self.get_admin_links(),
            'app_links': self.get_app_links(request)
        }
        return render(request, 'admin/frequency_report.html', context)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    ordering = ('id',)


@admin.register(OrderMeal)
class OrderMealView(admin.ModelAdmin):
    list_display = ('order', 'meal', 'amount',)
    list_filter = ('order_id',)
