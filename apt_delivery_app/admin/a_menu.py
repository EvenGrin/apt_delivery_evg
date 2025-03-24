import datetime

from django.contrib import admin

from apt_delivery_app.models import Menu


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('date',)
    filter_horizontal = ('meal',)
    date_hierarchy = "date"

    actions = ['copy_menu_to_today']
    @admin.action(description='Копировать выбранное меню на сегодня')
    def copy_menu_to_today(self, request, queryset):
        """
        Копирует выбранное меню на сегодняшнюю дату.
        """
        today = datetime.date.today()

        if Menu.objects.filter(date=today).exists():
            self.message_user(request, f"Меню на сегодня уже существует.", level="warning")
            return

        for menu in queryset:
            # Создаем копию меню с текущей датой
            new_menu = Menu.objects.create(date=today)

            # Добавляем блюда из исходного меню
            new_menu.meal.set(menu.meal.all())

            self.message_user(request, f"Копия меню от {menu.date} создана на сегодняшний день.")


