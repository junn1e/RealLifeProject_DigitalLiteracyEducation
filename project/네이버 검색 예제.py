import os
import sys
import urllib.request
import json
client_id = "0eNSo5Im5cqCzaFwINKm"  #클라이언트 ID
client_secret = "xC3azZJ4x6"        #클라이언트 시크릿 코드

searchWord = input()

encText = urllib.parse.quote(searchWord)
url = "https://openapi.naver.com/v1/search/news?query=" + encText # JSON 결과
# url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()    #서버 오류코드
if(rescode==200):
    response_body = response.read()
    #print(response_body.decode('utf-8'))

    response_body = json.loads(response_body.decode( 'utf-8' ))
    total = response_body["total"]
    print(total)

    count = 1
    for item in response_body["items"]:
        title   = item['title']
        pubDate = item['pubDate']
        link    = item['originallink']
        print("%d: %s / %s %s" %(count, pubDate, title, link))
        count += 1

else:
    print("Error Code:" + rescode)