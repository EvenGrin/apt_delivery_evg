from datetime import date

from django.urls import reverse
from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext

from apt_delivery_app.models import Meal, OrderMeal, Category, Menu


@admin.register(Meal)
class MealView(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'out', 'image', 'quantity', 'sold_meal_count')
    list_filter = ('category',)
    search_fields = ('name__iregex',)
    list_editable = ('quantity',)
    list_per_page = 10

    def sold_meal_count(self, obj):
        result = OrderMeal.objects.filter(meal=obj).count()
        return result

    sold_meal_count.short_description = "Количество заказанных"

    actions = ['create_menu']

    @admin.action(description="Добавить в меню на сегодня")
    def create_menu(self, request, queryset):
        menu = Menu.objects.filter(date=date.today())
        count = queryset.count()
        if menu:
            for i in queryset:
                menu[0].meal.add(i.id)
            url = (
                    reverse("admin:apt_delivery_app_menu_change", args={menu[0].id})
                    + "?"
                    + urlencode({"id": f"{menu[0].id}"})
            )
            self.message_user(request,
                              mark_safe(f"Добавлено {count} записи(ей) на <a href='{url}'>{menu[0].date}</a>."))
        else:
            menu = Menu.objects.create(date=date.today()).meal.set(queryset)
            url = (
                    reverse("admin:apt_delivery_app_menu_change", args={menu.id})
                    + "?"
                    + urlencode({"id": f"{menu[0].id}"})
            )
            self.message_user(request,
                              f"Создано {count} записи(ей) на на <a href='{url}'>{menu.date}</a>.")


@admin.register(Category)
class CategoryView(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name__iregex',)
