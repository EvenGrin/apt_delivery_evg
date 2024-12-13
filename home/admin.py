from django.contrib import admin
from home.models import Category, Meal, Menu


class MealView(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'out', 'image', 'quantity')

class MenuView(admin.ModelAdmin):
    list_display = ('date', 'meal')  # Add a custom display function




admin.site.register(Category)
admin.site.register(Meal, MealView)
admin.site.register(Menu, MenuView)