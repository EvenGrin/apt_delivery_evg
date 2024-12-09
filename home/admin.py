from django.contrib import admin
from home.models import Category, Meal, DayOfWeek, Menu


class MealView(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'out', 'image', 'quantity')

class MenuView(admin.ModelAdmin):
    list_display = ('meal', 'get_days_display')  # Add a custom display function

    def get_days_display(self, obj):
        return ", ".join([day.name for day in obj.days.all()])  #Custom function

    get_days_display.short_description = 'Days' #Sets the column header in admin

admin.site.register(Category)
admin.site.register(Meal, MealView)
admin.site.register(DayOfWeek)
admin.site.register(Menu, MenuView)
