import requests

API_KEY = "7ZJYB6CFY9X5SGSJ8VNQXXPDE"

def fetch_weather_data(city, start_date, end_date):
    """
    Fetch hourly weather data from Visual Crossing API
    """

    url = (
        f"https://weather.visualcrossing.com/"
        f"VisualCrossingWebServices/rest/services/timeline/"
        f"{city}/{start_date}/{end_date}"
    )

    params = {
        "unitGroup": "metric",
        "include": "hours",
        "key": API_KEY,
        "contentType": "json"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code}")

    return response.json()

def parse_hourly_data(api_response, city):
    """
    Convert API JSON into flat hourly records
    """

    records = []

    for day in api_response.get("days", []):
        date_value = day.get("datetime")

        for hour in day.get("hours", []):
            time_value = hour.get("datetime")
            temperature = hour.get("temp")

            record = {
                "city": city,
                "date": date_value,
                "time": time_value,
                "temperature": temperature,
            }

            records.append(record)

    return records

def calculate_aqi(temperature):
    """
    Calculate AQI based on temperature (academic logic)
    """

    if temperature <= 15:
        return 50
    elif 16 <= temperature <= 25:
        return 100
    elif 26 <= temperature <= 35:
        return 150
    elif 36 <= temperature <= 45:
        return 200
    else:
        return 300

def export_weather_to_csv():
    import csv
    import os
    from django.conf import settings
    from weather.models import WeatherData

    file_path = os.path.join(settings.BASE_DIR, "weather_data.csv")

    queryset = WeatherData.objects.all().order_by("date", "time")

    with open(file_path, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)

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

