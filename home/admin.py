from django.contrib import admin
from home.models import Category, Meal, MenuDay


class MealView(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'out', 'image', 'quantity')
    list_filter = ('category', )

# class MenuView(admin.ModelAdmin):
#     list_display = ('date', 'meal')  # Add a custom display function




admin.site.register(Category)
admin.site.register(Meal, MealView)
admin.site.register(MenuDay)