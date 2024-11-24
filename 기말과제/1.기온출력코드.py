import requests

API_KEY = "__apikey__"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(lat, lon):
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",
        "lang": "kr"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        current_temp = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        print(f"현재 온도: {current_temp}°C, 날씨: {weather_description}")
    else:
        print(f"API 호출 실패: {response.status_code}, {response.text}")


# 위도, 경도.
latitude = 37.5665
longitude = 126.9780
get_weather(latitude, longitude)
