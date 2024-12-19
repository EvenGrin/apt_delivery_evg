from django.contrib import admin
from django.db.models import Q

from home.models import Category, Meal, MenuDay

@admin.register(Meal)
class MealView(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'out', 'image', 'quantity')
    list_filter = ('category',)
    search_fields = ('name__iregex',)  # Case-insensitive search directly
# class MenuView(admin.ModelAdmin):
#     list_display = ('date', 'meal')  # Add a custom display function


admin.site.register(Category)
admin.site.register(MenuDay)
