import csv
import os
from django.conf import settings
from weather.models import WeatherData


def export_weather_to_csv():
    """
    Export WeatherData table to CSV file
    """

    file_path = os.path.join(settings.BASE_DIR, "weather_data.csv")

    queryset = WeatherData.objects.all().order_by("date", "time")

    with open(file_path, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)

        # CSV HEADER
        writer.writerow([
            "city",
            "date",
            "time",
            "temperature",
            "air_quality_index"
        ])

        for obj in queryset:
            writer.writerow([
                obj.city,
                obj.date.strftime("%Y-%m-%d"),
                obj.time.strftime("%H:%M"),
                obj.temperature,
                obj.air_quality_index
            ])

    return file_path

