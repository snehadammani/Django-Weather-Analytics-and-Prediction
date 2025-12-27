from django.contrib import admin
from .models import WeatherData

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = (
        "city",
        "date",
        "time",
        "temperature",
        "air_quality_index",
    )
    list_filter = ("city", "date")
    ordering = ("-date", "-time")

