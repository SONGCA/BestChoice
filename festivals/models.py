from django.db import models
from users.models import User

# 축제게시글 모델
class Festival_Article(models.Model):
    festival_title = models.CharField(max_length=50, default='')  #축제 제목
    festival_desc = models.TextField()  #축제 설명
    festival_address = models.CharField(max_length=50)  #축제 장소
    festival_region = models.CharField(max_length=50)  #축제 지역
    festival_date = models.CharField(max_length=50)  #축제 기간
    festival_image = models.CharField(max_length=100)  #축제 이미지
    festival_price = models.CharField(max_length=30)  # 축제 요금
    festival_cost = models.CharField(max_length=10)  # 무료 or 유료
    festival_start = models.DateField()  #시작일
    festival_end = models.DateField()  #종료일
    

# 축제게시글 북마크 모델
class Bookmark(models.Model):
    bookmark_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmark_set")  # 북마크한 사용자
    bookmark_festival = models.ForeignKey(Festival_Article, on_delete=models.CASCADE)  # 북마크한 축제게시글