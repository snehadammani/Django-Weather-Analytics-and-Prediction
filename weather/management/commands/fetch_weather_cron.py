from django.core.management.base import BaseCommand
from weather.views import fetch_weather
from django.test import RequestFactory

class Command(BaseCommand):
    help = "Fetch weather data and store in database (cron job)"

    def handle(self, *args, **kwargs):
        factory = RequestFactory()
        request = factory.get('/api/fetch-weather/')
        response = fetch_weather(request)
        self.stdout.write(self.style.SUCCESS("Weather data fetched successfully"))

