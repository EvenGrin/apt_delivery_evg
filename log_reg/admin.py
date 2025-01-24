import json

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.http import JsonResponse
from django.urls import path

from log_reg.models import User

@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'last_name', 'first_name', 'patronymic')
    list_filter = UserAdmin.list_filter
    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = (
            User.objects.annotate(date=TruncDay("date_joined"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [
            path("chart_data/", self.admin_site.admin_view(self.chart_data_endpoint))
        ]
        # NOTE! Our custom urls have to go before the default urls, because they
        # default ones match anything.
        return extra_urls + urls

    # JSON endpoint for generating chart data that is used for dynamic loading
    # via JS.
    def chart_data_endpoint(self, request):
        chart_data = self.chart_data()
        return JsonResponse(list(chart_data), safe=False)

    def chart_data(self):
        return (
            User.objects.annotate(date=TruncDay("date_joined"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )
# admin.site.register(User, UserAdmin)
