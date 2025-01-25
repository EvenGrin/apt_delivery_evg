from django.contrib import admin
from django.db.models import Q

from home.models import Category, Meal
from order.models import Order, OrderMeal


@admin.register(Meal)
class MealView(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'out', 'image', 'quantity', 'sold_meal_count')
    list_filter = ('category',)
    search_fields = ('name__iregex',)  # Case-insensitive search directly
    list_editable = ('quantity',)
    def sold_meal_count(self, obj):
        result = OrderMeal.objects.filter(meal=obj).count()
        return result
    # class MenuView(admin.ModelAdmin):
    sold_meal_count.short_description = "Количество заказанных"

#     list_display = ('date', 'meal')  # Add a custom display function


@admin.register(Category)
class CategoryView(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name__iregex',)  # Case-insensitive search directly
