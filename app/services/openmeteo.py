import requests
from flask import current_app
from app.services.weather_icon import WEATHER_ICON

def get_daily_weather(lat, lon, departure_date, return_date):
    url = current_app.config["OPENMETEO_URI"]

    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "Asia/Tokyo",
        "start_date": departure_date,
        "end_date": return_date
    }
    response = requests.get(url, params=params)
    data = response.json()

    daily = data["daily"]

    result = []
    for i in range(len(daily["time"])):
        code = daily["weathercode"][i]

        result.append({
            "date": daily["time"][i],
            "weather": WEATHER_ICON.get(code, {"label": "不明", "icon": "Question"}),
            "temp_max": daily["temperature_2m_max"][i],
            "temp_min": daily["temperature_2m_min"][i],
            "code": code
        })

    return result