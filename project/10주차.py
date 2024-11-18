from bs4 import BeautifulSoup
import urllib.request
import folium
import webbrowser
import random
import matplotlib.pyplot as plt

"""1교시 뷰티풀수프 실습 1
html_file = "coffee.html"
with open(html_file, "r", encoding="utf-8") as file:
  html = file.read()


soup = BeautifulSoup(html, "html.parser")

#print(soup.prettify())

#print(soup.h1)

tag_h1 = soup.h1
print(tag_h1)

tag_div = soup.div
print(tag_div)

tag_h1_all = soup.find_all("h1")
print(tag_h1_all)

tag_li_all = soup.find_all("li")
print(tag_li_all)

print(tag_h1.attrs)

tag_li = soup.li
print(tag_li)
print(tag_li.attrs)

print(tag_li['class'])

li_list = soup.select(".item_menu")
print(li_list)

for li in li_list:
  print(li.string)

"""
"""2교시 뷰티풀수프 실습 2
  print(parseData.h1)
print(parseData.find_all('li'))

print('타이틀:', parseData.title.string)
menu_list = parseData.select('div#coffeeMenu>ul>li.item>p.item-menu')
menu = menu_list[0] if menu_list else None
print(menu.string)
price_list = parseData.select('p.item-price')
for price in price_list:
    print(price.string)
"""
"""2교시 기상관측소 위치 리스트 뽑기
def main():
  #url = 'https://minwon.kma.go.kr/main/obvStn.do'링크가 안열려서 직접 다운반아서 열었습니다.
  # print(url)
  html_file = "기상관측소_위치.html"

  with open(html_file, "r", encoding="utf-8") as file:
    html = file.read()
  # print(html)
  soup = BeautifulSoup(html, 'html.parser')
  print(soup)
  result = []
  result = []
  tag_tbody = soup.find('tbody')
  
  for store in tag_tbody.find_all('tr'):
    store_td = store.find_all('td')
    store_loc = store_td[3].string
    store_address = store_td[4].string
    store_lat     = store_td[5].string
    store_att     = store_td[6].string
    
    result.append([store_loc]+[store_address]+[store_lat]+[store_att])
  print(result)

if __name__ == '__main__':
  main()
"""
"""3교시 지도 마커찍기

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
  position = [37.3921415, 126.9205866]
  map = folium.Map(location=position, zoom_start=15)
  
  for loc in result:
    popup = folium.Popup(loc[1], max_width=200) 
    folium.Marker(location=[float(loc[2]), float(loc[3])], popup=popup, icon=folium.Icon(color='red', icon='star')).add_to(map)
  
  map.save("map.html")
  webbrowser.open("map.html")

if __name__ == '__main__':
  main()
  showMap()
"""
"""3교시 로또 시뮬레이터
lotto = []
while True:
  temp = random.randrange(1,45)
  if lotto.count(temp)==0: # 중복 제거
    lotto.append(temp)
  if len(lotto)==6:
    break
        
print(lotto)

"""

y = []
for i in range(10):
  y.append(random.randrange(1,10))
x = range(len(y))

plt.title('random test')
plt.xlabel('sequence')
plt.ylabel('temperature')
plt.plot(x, y)
plt.show()
print(x)
print(x)