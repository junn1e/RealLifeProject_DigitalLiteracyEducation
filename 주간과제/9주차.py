import requests

def saveImage(fileName, imageUrl):
    imageResponse = requests.get(imageUrl, verify=False)
    if imageResponse.status_code == 200:
        with open('c:/users/82107/documents/실생활프로젝트/' + fileName, 'wb') as fout:
            fout.write(imageResponse.content)

def SearchImages(searchWord):
    url = 'https://dapi.kakao.com/v2/search/image'
    data = {
        'query': searchWord
    }
    headers = {
        'Authorization': 'KakaoAK 1134ece04f6cd6e3114ea58897ef03a8'
    }
    response = requests.get(url, data=data, headers=headers, verify=False)
    if response.status_code == 200:
        num = 1
        for document in response.json()['documents']:
            print('%d_%s' % (num, document['image_url']))
            fileName = '%s_%d.png' % (searchWord, num)
            imageUrl = document['image_url']
            saveImage(fileName, imageUrl)
            num += 1

searchWord = input('검색할 이미지 키워드 입력: ')
SearchImages(searchWord)
