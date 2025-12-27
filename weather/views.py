from datetime import date, timedelta, datetime
import requests
from django.http import JsonResponse
from weather.models import WeatherData
from django.http import FileResponse
from weather.utils import export_weather_to_csv


VISUAL_CROSSING_API_KEY = "7ZJYB6CFY9X5SGSJ8VNQXXPDE"


# -------------------------------
# STEP 3 / STEP 4 – DATA FETCH
# -------------------------------
def fetch_past_weather(request):
    CITY = "Hyderabad"

    end_date = date.today()
    start_date = end_date - timedelta(days=9)

    url = (
        f"https://weather.visualcrossing.com/VisualCrossingWebServices/"
        f"rest/services/timeline/{CITY}/"
        f"{start_date}/{end_date}"
        f"?unitGroup=metric&include=hours&key={VISUAL_CROSSING_API_KEY}&contentType=json"
    )

    response = requests.get(url, timeout=20)
    data = response.json()

    inserted = []

    for day in data.get("days", []):
        record_date = day["datetime"]  # YYYY-MM-DD

        for hour in day.get("hours", []):
            record_time = datetime.strptime(
                hour["datetime"], "%H:%M:%S"
            ).time()
            temperature = hour["temp"]

            # SIMPLE AQI LOGIC (project-safe)
            if temperature <= 20:
                aqi = 50
            elif temperature <= 30:
                aqi = 100
            else:
                aqi = 150

            WeatherData.objects.update_or_create(
                city=CITY,
                date=record_date,
                time=record_time,
                defaults={
                    "temperature": temperature,
                    "air_quality_index": aqi
                }
            )

            inserted.append(f"{record_date} {record_time}")

    return JsonResponse({
        "status": "success",
        "records_inserted": len(inserted),
    })


# -------------------------------
# STEP 5 – DATE BASED API
# -------------------------------
def weather_by_date(request):
    date_param = request.GET.get("date")

    if not date_param:
        return JsonResponse(
            {"error": "date query parameter is required (YYYY-MM-DD)"},
            status=400
        )

    records = WeatherData.objects.filter(
        date=date_param
    ).order_by("time")

    if not records.exists():
        return JsonResponse(
            {"message": "No data found for this date"},
            status=404
        )

    data_array = []

    for r in records:
        data_array.append({
            "time": r.time.strftime("%H:%M"),
            "temperature": r.temperature,
            "air_quality_index": r.air_quality_index
        })

    return JsonResponse({
        "city": records[0].city,
        "date": date_param,
        "total_records": len(data_array),
        "data": data_array
    })


# -------------------------------
# STEP 5 – TIME BASED API
# -------------------------------
def weather_by_time(request):
    time_param = request.GET.get("time")

    if not time_param:
        return JsonResponse(
            {"error": "time query parameter is required (HH:MM)"},
            status=400
        )

    records = WeatherData.objects.filter(
        time=time_param
    ).order_by("date")

    if not records.exists():
        return JsonResponse(
            {"message": "No data found for this time"},
            status=404
        )

    data_array = []

    for r in records:
        data_array.append({
            "date": r.date.strftime("%Y-%m-%d"),
            "temperature": r.temperature,
            "air_quality_index": r.air_quality_index
        })

    return JsonResponse({
        "city": records[0].city,
        "time": time_param,
        "total_records": len(data_array),
        "data": data_array
    })


# -------------------------------
# STEP 5.5 – FINAL GENERIC API
# -------------------------------
def weather_data_api(request):
    """
    API to fetch weather data with filters
    """

    queryset = WeatherData.objects.all().order_by("date", "time")

    city = request.GET.get("city")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    time = request.GET.get("time")

    if city:
        queryset = queryset.filter(city=city)

    if start_date:
        queryset = queryset.filter(date__gte=start_date)

    if end_date:
        queryset = queryset.filter(date__lte=end_date)

    if time:
        queryset = queryset.filter(time=time)

    data = []
    for obj in queryset:
        data.append({
            "city": obj.city,
            "date": obj.date.strftime("%Y-%m-%d"),   # ✅ STEP 5.5 FIX
            "time": obj.time.strftime("%H:%M"),      # ✅ STEP 5.5 FIX
            "temperature": obj.temperature,
            "air_quality_index": obj.air_quality_index,
        })

    return JsonResponse(data, safe=False)

def download_weather_csv(request):
    """
    API to download weather data CSV
    """
    file_path = export_weather_to_csv()

    return FileResponse(
        open(file_path, "rb"),
        as_attachment=True,
        filename="weather_data.csv"
    )
