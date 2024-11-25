import requests
import openai
from datetime import datetime, timezone, timedelta

# API 키
GOOGLE_API_KEY = ""
WEATHERMAP_API_KEY = ""
openai.api_key = ""

# API URL
WEATHERMAP_ONECALL_URL = "https://api.openweathermap.org/data/3.0/onecall"
AIR_POLLUTION_URL = "https://api.openweathermap.org/data/2.5/air_pollution"
GEOCODING_URL = "https://maps.googleapis.com/maps/api/geocode/json"

def get_weather(lat, lon):
    # Google Maps API 요청 (주소 정보)
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

    # OpenWeatherMap One Call API 요청 (날씨 정보)
    weather_params = {
        "lat": lat,
        "lon": lon,
        "appid": WEATHERMAP_API_KEY,
        "units": "metric",
        "exclude": "minutely",
        "lang": "kr"
    }
    weather_response = requests.get(WEATHERMAP_ONECALL_URL, params=weather_params)

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

    # OpenWeatherMap Air Pollution API 요청 (대기오염 정보)
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

    # 시간별 예보 데이터 변환
    forecast = []
    for hour in hourly_data:
        forecast.append({
            "dt": datetime.fromtimestamp(hour["dt"], kst).strftime('%H시'),
            "temp": hour.get("temp"),
            "weather": hour.get("weather", [{}])[0].get("description", ""),
            "icon": hour.get("weather", [{}])[0].get("icon", ""),
            "pop": hour.get("pop", 0)
        })

    # 결과 반환
    result = {
        "address": formatted_address,
        "weather_current": {
            "temperature": temp,
            "temp_feel": feels_like,
            "contition": weather_condition,
            "sunrise": sunrise,
            "sunset": sunset,
            "uv_index": max_uvi,  # 최대 UV 지수 사용
            "precipitation": precipitation,
            "air_quality": pm2_5
        },
        "forecast": forecast
    }
    return result

# openAI API 요청 (기상상황 리뷰)
def makeAnswer(weather_info):
    # 데이터 추출
    address = weather_info.get("address", "알 수 없는 주소")
    current_weather = weather_info.get("weather_current", {})
    temperature = current_weather.get("temperature", "N/A")
    temp_feel = current_weather.get("temp_feel", "N/A")
    condition = current_weather.get("contition", "N/A")
    air_quality = current_weather.get("air_quality", "N/A")
    precipitation = current_weather.get("precipitation", "N/A")
    uv_index = current_weather.get("uv_index", "N/A")
    sunrise = current_weather.get("sunrise", "N/A")
    sunset = current_weather.get("sunset", "N/A")
    forecast = weather_info.get("forecast", [])

    # 시간별 예보 요약
    forecast_summary = "\n".join([
        f"{hour['dt']}: {hour['temp']}°C, {hour['weather']} (강수 확률: {hour['pop'] * 100:.0f}%)"
        for hour in forecast[:12]
    ])

    # !질문 구성!
    question = f"""
    나는 {address}에 거주하는 사용자에게 개인 기상 비서처럼 날씨 정보를 리뷰하고, 날씨에 따른 행동을 조언하는 역할을 하고 싶어.
    현재 {address}의 날씨 정보는 다음과 같아:
    - 현재 기온: {temperature}°C, 체감 온도: {temp_feel}°C
    - 날씨 상태: {condition}
    - 일출 시간: {sunrise}, 일몰 시간: {sunset}
    - 강수량: {precipitation}mm
    - 자외선 지수: {uv_index}
    - 대기질(PM2.5): {air_quality}

    그리고 앞으로 6시간 동안의 날씨 예보는 다음과 같아:
    {forecast_summary}

    이 정보를 바탕으로 아래 요구를 만족하는 답변을 작성해 줘:
    1. 현재 날씨를 바탕으로 한 종합적인 리뷰 작성.
    2. 사용자가 알아두면 좋은 포인트 강조 (예: 비가 온다면 우산, 대기질 나쁨 시 마스크 등).
    3. 시간별 예보에 따라 어떤 시간대에 비가 올 가능성이 높은지, 야외활동에 적합한 시간을 언급.
    4. 사용자가 그 날에 입으면 좋을 옷을 추천해 줘. 예를 들어, 기온이 낮으면 따뜻한 옷을, 일교차가 크다면 쉽게 입고 벗을 수 있는 겉옷을, 자외선이 강하면 가벼운 옷과 모자를 추천.
    답변을 최대한 친근하면서도 유용한 톤으로 작성해 줘. 
    """

    # OpenAI API 호출
    response = openai.ChatCompletion.create(
        model="gpt-4",  # 모델 변경
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question.strip()}
        ],
        max_tokens=1000,  # 토큰 수 조정
        temperature=0.7,  # 창의성 수준
    )

    # 답변 추출
    result = response['choices'][0]['message']['content'].strip()
    return result



# 테스트 실행
try:
    lat, lon = 37.5665, 126.9780  # 서울의 위도와 경도 예제
    weather_info = get_weather(lat, lon)
    answer = makeAnswer(weather_info)
    weather_info["answer"] = answer
    # 출력
    print(answer)
except Exception as e:
    print(f"오류: {e}")