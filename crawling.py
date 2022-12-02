import requests
from bs4 import BeautifulSoup

# range를 이용하면 0부터 인덱스가 시작되므로 page_num에 1을 더해준 url을 이용
festival_id = 1
for page_num in range(8):
    url = f'https://www.mcst.go.kr/kor/s_culture/festival/festivalList.jsp?pCurrentPage={page_num+1}'
    headers = {'User-Agent': 'Chrome'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    if page_num != 7:
        for num in range(5):
            data = soup.select(f"#content > div.contentWrap > ul > li:nth-child({num+1})")
            # 리스트에서 뽑기
            for item in data:
                title = item.select_one('div.text > p').text
                link = item.select_one('a').get('href')
                desc = item.select_one('div.text > div').text.replace('\r\n', '')
                period = item.select_one('div.text > ul > li:nth-child(1)').text
            result_url = 'https://www.mcst.go.kr/kor/s_culture/festival/' + link

            headers2 = {'User-Agent': 'Chrome'}
            response2 = requests.get(result_url, headers=headers2)
            soup2 = BeautifulSoup(response2.text, 'html.parser')

            data2 = soup2.select("#content > div.contentWrap > div.viewWarp")
            
            # 상세페이지에서 뽑기
            for item in data2:
                image= 'https://www.mcst.go.kr' + item.select_one('img').get('src')
                region= item.select_one('dl > dd:nth-child(2)').text
                place = item.select_one('dl > dd:nth-child(10)').text
                price = item.select_one('dl > dd:nth-child(12)').text
                
                festival_data = [festival_id, title, desc, image, region, place, price, period]
                print(festival_data)
            festival_id += 1
                
                
    else:  # 마지막 페이지는 4번만 반복
        for num in range(4):
            data = soup.select(f"#content > div.contentWrap > ul > li:nth-child({num+1})")
            for item in data:
                title = item.select_one('div.text > p').text
                link = item.select_one('a').get('href')
                desc = item.select_one('div.text > div').text.replace('\r\n', '')
                period = item.select_one('div.text > ul > li:nth-child(1)').text
            result_url = 'https://www.mcst.go.kr/kor/s_culture/festival/' + link

            headers2 = {'User-Agent': 'Chrome'}
            response2 = requests.get(result_url, headers=headers2)
            soup2 = BeautifulSoup(response2.text, 'html.parser')

            data2 = soup2.select("#content > div.contentWrap > div.viewWarp")
            
            for item in data2:
                image= 'https://www.mcst.go.kr' + item.select_one('img').get('src')
                region= item.select_one('dl > dd:nth-child(2)').text
                place = item.select_one('dl > dd:nth-child(10)').text
                price = item.select_one('dl > dd:nth-child(12)').text
                
                festival_data = [festival_id, title, desc, image, region, place, price, period]
                print(festival_data)
            festival_id += 1