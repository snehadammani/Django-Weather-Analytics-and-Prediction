from django.db import models

class WeatherData(models.Model):
    city = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    temperature = models.FloatField()
    air_quality_index = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} - {self.date} {self.time}"

