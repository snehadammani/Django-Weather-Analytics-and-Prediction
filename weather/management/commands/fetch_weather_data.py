from django.core.management.base import BaseCommand
from weather.services import save_weather_data

class Command(BaseCommand):
    help = "Fetch and save weather data automatically"

    def handle(self, *args, **kwargs):
        saved = save_weather_data()
        self.stdout.write(
            self.style.SUCCESS(
                f"Weather data fetch complete. Rows inserted: {saved}"
            )
        )

