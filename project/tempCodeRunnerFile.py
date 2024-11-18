

result = []

def main():    
  html_file = "기상관측소_위치.html"

  with open(html_file, "r", encoding="utf-8") as file:
    html = file.read()

  soup = BeautifulSoup(html, 'html.parser')

  tag_tbody = soup.find('tbody')

  for store in tag_tbody.find_all('tr'):
      store_td = store.find_all('td')
      store_loc = store_td[3].string
      store_address = store_td[4].string
      store_lat = store_td[5].string
      store_att = store_td[6].string
      
      result.append([store_loc] + [store_address] + [store_lat] + [store_att])

  print(result)

def showMap():
    print('관측소 맵에 표시합니다')
    position = [37.3921415, 126.9205866]  # 위치 수정
    map = folium.Map(location=position, zoom_start=15)
    
    for loc in result:
        popup = folium.Popup(loc[1], max_width=200)  # 수정: loc[1]으로 주소 표시
        folium.Marker(location=[float(loc[2]), float(loc[3])], popup=popup, icon=folium.Icon(color='red', icon='star')).add_to(map)
    
    map.save("map.html")  # 저장 파일명 수정
    webbrowser.open("map.html")  # 파일 열기

if __name__ == '__main__':
    main()
    showMap()
