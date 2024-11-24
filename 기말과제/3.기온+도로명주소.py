import geocoder
import requests

# OpenWeatherMap API 키
WEATHERMAP_API_KEY = "_"
WEATHERMAP_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# 네이버 클라우드 플랫폼 Reverse Geocode API 키
NAVER_CLIENT_ID = "048yod4phr"
NAVER_CLIENT_SECRET = "_"

# Google Geolocation API 키
GOOGLE_API_KEY = "_"
GOOGLE_URL = f"https://www.googleapis.com/geolocation/v1/geolocate?key={GOOGLE_API_KEY}"

# 하는 일: 전달받은 좌표의 기온과 날씨 반환
def get_weather(lat, lon):
    params = {
        "lat": lat,
        "lon": lon,
        "appid": WEATHERMAP_API_KEY,
        "units": "metric",
        "lang": "kr"
    }
    response = requests.get(WEATHERMAP_BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        current_temp = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        return f"현재 온도: {current_temp}°C, 날씨: {weather_description}"
    else:
        raise Exception(f"날씨 정보를 가져오는 데 실패했습니다. 상태 코드: {response.status_code}, 메시지: {response.text}")

# 하는 일: 전달받은 좌표의 시, 군/구, 도로명주소 반환
def get_address(lat, lon):
    url = "https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": NAVER_CLIENT_ID,
        "X-NCP-APIGW-API-KEY": NAVER_CLIENT_SECRET
    }
    params = {
        "coords": f"{lon},{lat}",  # 경도, 위도 순서
        "orders": "legalcode,admcode,addr,roadaddr",  # 반환 데이터 타입
        "output": "json"  # JSON 형식으로 출력
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        # 행정구역 (시/군/구) 정보 추출
        region = data["results"][0]["region"]
        si = region["area1"]["name"]
        gu = region["area2"]["name"]
        dong = region["area3"]["name"]
        return f"{si} {gu} {dong}"
    else:
        raise Exception(f"주소 정보를 가져오는 데 실패했습니다. 상태 코드: {response.status_code}, 메시지: {response.text}")

# 하는 일: 좌표 반환
def get_coord():
    response = requests.post(GOOGLE_URL, json={})
    location = response.json()

    if "location" in location:
        lat = location["location"]["lat"]
        lon = location["location"]["lng"]
        return lat, lon
    else:
        location = geocoder.ip('me')

        if location.ok:
            lat, lon = location.latlng[0], location.latlng[1]
            return lat, lon
        else:
            raise Exception("위치 정보를 가져오는 데 실패했습니다.")

# 실행
try:
    lat, lon = get_coord()
    #print(f"현재 위치의 위도: {lat}, 경도: {lon}")
    print(f"주소: {get_address(lat, lon)}")
    print(f"날씨 정보: {get_weather(lat, lon)}")
except Exception as e:
    print(f"오류: {e}")
