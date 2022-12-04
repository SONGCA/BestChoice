import requests
from bs4 import BeautifulSoup
import csv

# range를 이용하면 0부터 인덱스가 시작되므로 page_num에 1을 더해준 url을 이용
filename = 'festival_list.csv'
f = open(filename, 'w', encoding='utf-8-sig', newline='')
writer = csv.writer(f)

titles = ['festivalId', 'festival_title', 'festival_desc', 'festival_image', 'festival_region', 'festival_place', 'festival_price', 'festival_period']
writer.writerow(titles)

festival_id = 1
for page_num in range(163):
    url = f'https://www.mcst.go.kr/kor/s_culture/festival/festivalList.jsp?pMenuCD=&pCurrentPage={page_num+1}&pSearchType=01&pSearchWord=&pSeq=&pSido=&pOrder=01up&pPeriod=&fromDt=20220101&toDt=20221231'
    headers = {'User-Agent': 'Chrome'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

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
            writer.writerow(festival_data)
        festival_id += 1
                