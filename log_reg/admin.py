from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from log_reg.models import User


@admin.register(User)
class UsersAdmin(UserAdmin):
    list_display = ('username', 'email', 'last_name', 'first_name', 'patronymic')
    list_filter = UserAdmin.list_filter
    fieldsets = list(UserAdmin.fieldsets)
    fieldsets[1] = (fieldsets[1][0], {'fields': ('last_name', 'first_name', 'patronymic', 'email')})
    search_fields = ('last_name__iregex', 'first_name__iregex', 'patronymic__iregex')
