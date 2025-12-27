from datetime import date, timedelta

from weather.models import WeatherData
from weather.utils import (
    fetch_weather_data,
    parse_hourly_data,
    calculate_aqi
)


def save_weather_data():
    """
    Fetch weather data (past 10 days + today + tomorrow)
    and save hourly records into SQLite safely.
    """

    city = "Hyderabad"

    # -------------------------
    # DATE CALCULATION
    # -------------------------
    today = date.today()
    tomorrow = today + timedelta(days=1)

    past_10_days = []
    for i in range(10, 0, -1):
        past_10_days.append(today - timedelta(days=i))

    # ONLY allowed dates
    all_dates = past_10_days + [today, tomorrow]
    allowed_dates = set(all_dates)

    start_date = all_dates[0]
    end_date = all_dates[-1]

    # -------------------------
    # FETCH API DATA
    # -------------------------
    api_response = fetch_weather_data(city, start_date, end_date)

    # -------------------------
    # PARSE HOURLY DATA
    # -------------------------
    records = parse_hourly_data(api_response, city)

    saved_count = 0

    # -------------------------
    # SAVE TO DATABASE
    # -------------------------
    for record in records:

        # 🚫 BLOCK unwanted future dates (26, 27, etc.)
        if record["date"] not in allowed_dates:
            continue

        temperature = record["temperature"]
        aqi = calculate_aqi(temperature)

        # 🚫 DUPLICATE CHECK
        exists = WeatherData.objects.filter(
            city=record["city"],
            date=record["date"],
            time=record["time"]
        ).exists()

        if not exists:
            WeatherData.objects.create(
                city=record["city"],
                date=record["date"],
                time=record["time"],
                temperature=temperature,
                air_quality_index=aqi
            )
            saved_count += 1

    return saved_count

