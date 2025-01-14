from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from log_reg.models import User

@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'last_name', 'first_name', 'patronymic')


# admin.site.register(User, UserAdmin)
