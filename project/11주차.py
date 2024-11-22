from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
import time

# 해당 url의 정보(매장)들을 shopData.csv파일로 저장하기.
"""
result = []

def main():
    for page in range(1, 5):
        url = 'https://www.hollys.co.kr/store/korea/korStore2.do?pageNo=%d&sido=&gugun=&store='%page
        #print(url)
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        #print(soup)
        
        tag_tbody = soup.find('tbody')
        for store in tag_tbody.find_all('tr'):
            store_td = store.find_all('td')
            store_name = store_td[1].string
            store_address = store_td[3].string
            store_address = store_address[:store_td[3].string.find('(')]
            store_tel = store_td[5].string
            result.append([store_name]+[store_address]+[store_tel])
            
    #print(result)
    
    df = pd.DataFrame(result, columns=['매장명','주소','전화번호'])
    df.to_csv('shopData.csv', encoding='utf-8', mode='w', index=False)
    print('csv file saved...')

if __name__ == '__main__':
     main()
"""

# 브라우저 열기..
"""
wd = webdriver.Chrome()
wd.get('https://www.coffeebeankorea.com/store/store.asp')

try:
    #wd.execute_script('storePop2("29")')
    html = wd.page_source
    soup = BeautifulSoup(html,'html.parser')
    input("")
except:
    pass 
"""

wd = webdriver.Chrome()
result = []

for id in range(1, 20):
    wd.get('https://www.coffeebeankorea.com/store/store.asp')

    try:
        wd.execute_script('storePop2(%d)' % id)
        print(f"storePop2({id}) 실행")

        WebDriverWait(wd, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.store_txt > h2"))
        )

        html = wd.page_source
        soup = BeautifulSoup(html, 'html.parser')

        store_name_h2 = soup.select("div.store_txt > h2")
        store_name = store_name_h2[0].string if store_name_h2 else "정보 없음"

        store_info = soup.select("div.store_txt > table.store_table > tbody > tr > td")
        if len(store_info) >= 4:
            store_address_list = list(store_info[2])
            store_address = store_address_list[0] if store_address_list else "정보 없음"
            store_phone = store_info[3].string if store_info[3] else "정보 없음"
        else:
            store_address = "정보 없음"
            store_phone = "정보 없음"

        result.append([store_name, store_address, store_phone])
        print(f"{store_name}, {store_address}, {store_phone} 저장 완료")

    except Exception as e:
        print(f"Error for store ID {id}: {e}")
        continue

try:
    df = pd.DataFrame(result, columns=['매장명', '주소', '전화번호'])
    df.to_csv('coffeebean.csv', encoding='utf-8', mode='w', index=False)
    print('CSV 파일 저장 완료: coffeebean.csv')
except Exception as e:
    print(f"CSV 저장 실패: {e}")

wd.quit()
