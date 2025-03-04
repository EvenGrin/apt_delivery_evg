from datetime import date

from django.contrib import admin

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
        menu =Menu.objects.filter(date=date.today())
        if menu:
            for i in queryset:
                menu[0].meal.add(i.id)
        else:
            Menu.objects.create(date=date.today()).meal.set(queryset)


@admin.register(Category)
class CategoryView(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name__iregex',)