import requests

# 네이버 API 키 설정
CLIENT_ID = "048yod4phr"
CLIENT_SECRET = ""

def get_address(lat, lon):
    url = "https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": CLIENT_ID,
        "X-NCP-APIGW-API-KEY": CLIENT_SECRET
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
        return "주소 정보를 가져오는 데 실패했습니다."

# 예시: 위도와 경도 입력
latitude = 37.5665  # 서울 위도
longitude = 126.9780  # 서울 경도
address = get_address(latitude, longitude)
print(f"현재 위치: {address}")
