from django.contrib import admin
from .models import EGYNationalIDInfo, APILog

@admin.register(EGYNationalIDInfo)
class EGYNationalIDInfoAdmin(admin.ModelAdmin):
    list_display = ("national_id", "birth_year", "birth_month", "birth_day")
    search_fields = ("national_id",)
    list_filter = ("birth_year", "birth_month")

@admin.register(APILog)
class APILogAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "national_id", "timestamp")
    search_fields = ("national_id",)
    list_filter = ("timestamp",)
