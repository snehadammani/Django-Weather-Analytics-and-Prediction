from django.urls import path
from . import views

urlpatterns = [
    path('fetch-past-weather/', views.fetch_past_weather, name='fetch_past_weather'),
    path('weather/', views.weather_data_api, name='weather_data_api'),
    path('weather-by-date/', views.weather_by_date, name='weather_by_date'),
    path('weather-by-time/', views.weather_by_time, name='weather_by_time'),
    path('download-weather-csv/', views.download_weather_csv, name='download_weather_csv'),
]

