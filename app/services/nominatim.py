import requests
from flask import current_app

def geocode(destination):
    url = current_app.config["NOMINATIM_URI"]

    params = {"q": destination, "format": "json", "limit": 1}

    # ヘッダー(APIポリシーに従う)
    headers = {
        "User-Agent": "PackCompApp/1.0"
    }
    response = requests.get(url, params=params, headers=headers)

    data = response.json()
    if not data:
        return None, None
    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])
    return lat, lon
