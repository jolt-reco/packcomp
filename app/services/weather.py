import requests
from flask import current_app
from datetime import datetime, timedelta
from collections import Counter

def get_forecast(destination, departure_date, return_date):
    
    # city: 都市名
    # travel_date: 'YYYY-MM-DD' 形式
    url = current_app.config["WEATHER_FORECAST_URL"]
    params = {
        "q": destination,
        "appid": current_app.config["WEATHER_API_KEY"],
        "units": "metric",
        "lang": "ja"
    }

    res = requests.get(url, params=params)
    data = res.json()

    day_count = min((return_date - departure_date).days + 1, 5)

    result = {}
    for i in range(day_count):
        target_date = departure_date + timedelta(days=i)
        target_resp = [
            item for item in data.get("list", [])
            if datetime.fromtimestamp(item["dt"]).date() == target_date
        ]                                                                                            
        if target_resp:
            result[target_date.strftime("%Y-%m-%d")] = target_resp

    return result


def summarize_forecast(forecast_data):

    weather_list = [item["weather"][0]["main"] for item in forecast_data]
    unique_ordered = []
    for w in weather_list:
        if w not in unique_ordered:
            unique_ordered.append(w)

    if len(unique_ordered) == 1:
        return unique_ordered[0]
    elif len(unique_ordered) == 2:
        return f"{unique_ordered[0]}のち{unique_ordered[1]}" 
    else:
        return "ときどき".join(unique_ordered)
    

def get_summary_for_travel(destination, departure_date, return_date):

    raw = get_forecast(destination, departure_date, return_date)
    summary_dict = {
        date: summarize_forecast(forecast_data) for date, forecast_data in raw.items()
    }
    return summary_dict