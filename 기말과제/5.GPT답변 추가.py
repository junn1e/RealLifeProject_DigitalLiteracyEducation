import requests
from datetime import datetime, timezone, timedelta

# api키
GOOGLE_API_KEY = ""
WEATHERMAP_API_KEY = ""
# api url
WEATHERMAP_ONECALL_URL = "https://api.openweathermap.org/data/3.0/onecall"
AIR_POLLUTION_URL = "https://api.openweathermap.org/data/2.5/air_pollution"
GEOCODING_URL = "https://maps.googleapis.com/maps/api/geocode/json"



def get_weather(lat, lon):
    # 1. formatted_address 에 주소 정보 저장 (Google Maps)
    geo_url = f"{GEOCODING_URL}?latlng={lat},{lon}&key={GOOGLE_API_KEY}"
    geo_response = requests.get(geo_url)
    if geo_response.status_code == 200:
        geo_data = geo_response.json()
        if "results" in geo_data and len(geo_data["results"]) > 0:
            formatted_address = geo_data["results"][0].get("formatted_address", "주소를 찾을 수 없습니다.")
        else:
            formatted_address = "주소를 찾을 수 없습니다."
    else:
        raise Exception(f"Google Maps API 요청 실패, 상태 코드: {geo_response.status_code}")

    # 2. pm2_5 에 미세먼지 데이터 저장 (OpenWeatherMap Air Pollution)
    air_pollution_params = {
        "lat": lat,
        "lon": lon,
        "appid": WEATHERMAP_API_KEY
    }
    air_pollution_response = requests.get(AIR_POLLUTION_URL, params=air_pollution_params)

    if air_pollution_response.status_code == 200:
        air_pollution_data = air_pollution_response.json()
        pm2_5 = air_pollution_data["list"][0]["components"]["pm2_5"]
    else:
        pm2_5 = "N/A"

    # 3. weather_response 에 날씨 데이터 저장 (OpenWeatherMap One Call)
    weather_params = {
        "lat": lat,
        "lon": lon,
        "appid": WEATHERMAP_API_KEY,
        "units": "metric",
        "exclude": "minutely",
        "lang": "kr"
    }
    weather_response = requests.get(WEATHERMAP_ONECALL_URL, params=weather_params)

    # 4. 날씨 데이터에서 정보 추출
    if weather_response.status_code == 200:
        weather_data = weather_response.json()

        # 현재 날씨 정보
        current = weather_data["current"]
        temp = current["temp"]
        feels_like = current["feels_like"]
        weather_condition = current["weather"][0]["description"]

        # UTC 시간대를 KST(UTC+9)로 변환
        kst = timezone(timedelta(hours=9))
        sunrise = datetime.fromtimestamp(current["sunrise"], kst).strftime('%Y-%m-%d %H:%M:%S')
        sunset = datetime.fromtimestamp(current["sunset"], kst).strftime('%Y-%m-%d %H:%M:%S')
        precipitation = current.get("rain", {}).get("1h", 0.0) or current.get("snow", {}).get("1h", 0.0)

        # 시간별 및 일별 데이터
        hourly_data = weather_data.get("hourly", [])[:12]  # 최대 48시간

        # 시간별 UV 지수에서 최대값 찾기
        max_uvi = max((hour.get("uvi", 0) for hour in hourly_data), default=0)

    else:
        raise Exception(f"OpenWeatherMap One Call API 요청 실패, 상태 코드: {weather_response.status_code}")

    # 5. forecast[]에 시간별 예보 정보 저장
    forecast = []
    for hour in hourly_data:
        forecast.append({
            "dt": datetime.fromtimestamp(hour["dt"], kst).strftime('%H시'),
            "temp": hour.get("temp"),
            "weather": hour.get("weather", [{}])[0].get("description", ""),
            "icon": hour.get("weather", [{}])[0].get("icon", ""),
            "pop": hour.get("pop", 0)
        })

    # 6. 질문 작성
    forecast_summary = "\n".join([f"{hour['dt']}: {hour['temp']}°C, {hour['weather']} (강수 확률: {hour['pop'] * 100:.0f}%)" for hour in forecast[:12]])

    # 질문 구성
    question = f"""
    역할 : 너는 {formatted_address}에 거주하는 사용자에게 개인 기상 비서처럼 날씨 정보를 리뷰하고, 날씨에 따른 행동을 조언하는 역할이야.
    답변 양식 :
    - 친근하고 유용한 톤으로, 현재 날씨를 바탕으로 한 종합적인 리뷰를 작성해. 중간중간에 사용자가 알아두면 좋은 포인트를 알려줘. (예: 비가 온다면 우산, 대기질 나쁨 시 마스크 등). 100자 내지 200자 이내로 작성할 것.
    - 활동 시간 추천 : 시간별 예보에 따라 어떤 시간대에 비가 올 가능성이 높은지, 야외활동에 적합한 시간을 언급해 줘. 50자 내지 100자 이내로 작성할 것.
    - 옷차림 추천 : 사용자가 그 날에 입으면 좋을 옷을 추천해 줘. 예를 들어, 기온이 낮으면 따뜻한 옷을, 일교차가 크다면 쉽게 입고 벗을 수 있는 겉옷을, 자외선이 강하면 가벼운 옷과 모자를 추천. 50자 내지 100자 이내로 작성할 것.
    날씨 정보 : {formatted_address}의 현재 날씨는 다음과 같아. 기온: {temp}도, 체감 온도: {feels_like}도, 기상 상태: {weather_condition}, 일출: {sunrise}, 일몰: {sunset}, 강수량: {precipitation}mm, 자외선 지수: {max_uvi}, 대기질(PM2.5): {pm2_5}.
    날씨 예보 : 6시간 뒤 까지의 날씨 데이터는 다음과 같아. {forecast_summary}
    """

    # 6. 결과 반환
    result = {
        "address": formatted_address,
        "weather_current": {
            "temperature": temp,
            "temp_feel": feels_like,
            "condition": weather_condition,
            "sunrise": sunrise,
            "sunset": sunset,
            "uv_index": max_uvi,
            "precipitation": precipitation,
            "air_quality": pm2_5
        },
        "forecast": forecast,
        "question" : question
    }
    return result