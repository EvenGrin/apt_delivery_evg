from django.contrib import admin

from apt_delivery_app.models import Menu


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('date',)
    filter_horizontal = ('meal',)
    list_filter = ('id',)

