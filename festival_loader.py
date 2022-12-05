import os
import sys
import csv
import django

#환경변수 세팅(뒷부분은 프로젝트명.settings로 설정한다.)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bestchoice.settings")
django.setup()
# model import
from articles.models import *

#읽어들일 csv 디렉토리를 각 변수에 담는다.
festival = 'festival_list.csv'

#함수 정의하기 (row부분엔 해당 table의 row명을 적어준다.)
def festival_loader():
    with open(festival, 'rt', encoding='cp949') as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        for row in data_reader:
            if row[0]:
                festival_title = row[1]
                festival_desc = row[2]
                festival_image = row[3]
                festival_region = row[4]
                festival_address = row[5]
                festival_price = row[6]
                festival_date = row[7]


                print(festival_title, festival_desc, festival_image, festival_region, festival_address, festival_price, festival_date)
                Festival_Article.objects.create(
                    festival_title = festival_title,
                    festival_desc = festival_desc,
                    festival_image = festival_image,
                    festival_region = festival_region,
                    festival_address = festival_address,
                    festival_price = festival_price,
                    festival_date = festival_date
                    )
    print('PRODUCT DATA UPLOADED SUCCESSFULY!')

# 함수 실행
festival_loader()