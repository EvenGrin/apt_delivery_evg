from django.contrib import admin
from home.models import Category, Meal


class MealView(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'out', 'image', 'quantity')


admin.site.register(Category)
admin.site.register(Meal, MealView)
