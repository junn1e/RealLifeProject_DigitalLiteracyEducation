#script.py

import requests

# Google Geolocation API 키
GOOGLE_API_KEY = "__"

# OpenWeatherMap API 키
WEATHERMAP_API_KEY = "__"
WEATHERMAP_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(lat, lon):
    # Google Maps API 요청 (주소 정보)
    geo_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={GOOGLE_API_KEY}"
    geo_response = requests.get(geo_url)
    
    if geo_response.status_code == 200:
        geo_data = geo_response.json()
        if "results" in geo_data and len(geo_data["results"]) > 0:
            formatted_address = geo_data["results"][0].get("formatted_address", "주소를 찾을 수 없습니다.")
        else:
            formatted_address = "주소를 찾을 수 없습니다."
    else:
        raise Exception(f"Google Maps API 요청 실패, 상태 코드: {geo_response.status_code}")

    # OpenWeatherMap API 요청 (날씨 정보)
    weather_params = {
        "lat": lat,
        "lon": lon,
        "appid": WEATHERMAP_API_KEY,
        "units": "metric",
        "lang": "kr"
    }
    weather_response = requests.get(WEATHERMAP_BASE_URL, params=weather_params)

    if weather_response.status_code == 200:
        weather_data = weather_response.json()
        weather_temperature = weather_data["main"]["temp"]
        weather_condition = weather_data["weather"][0]["description"]
    else:
        raise Exception(f"OpenWeatherMap API 요청 실패, 상태 코드: {weather_response.status_code}, 메시지: {weather_response.text}")

    # 결과 반환
    result = {
        "address": formatted_address,
        "temperature": weather_temperature,
        "condition": weather_condition
    }
    return result

# 테스트 실행
try:
    lat, lon = 37.5665, 126.9780  # 서울의 위도와 경도 예제
    weather_info = get_weather(lat, lon)
    print(f"주소: {weather_info['address']}")
    print(f"현재 온도: {weather_info['temperature']}°C")
    print(f"날씨 상태: {weather_info['condition']}")
except Exception as e:
    print(f"오류: {e}")
