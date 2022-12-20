from django.db import models
from users.models import User
from festivals.models import Festival_Article


# 모집게시글 모델
class Join_Article(models.Model):
    join_author = models.ForeignKey(User, verbose_name="작성자", on_delete=models.CASCADE)  #모집 작성자
    join_festival = models.ForeignKey(Festival_Article, verbose_name="축제", on_delete=models.CASCADE)  #모집 축제
    join_title = models.CharField(max_length=20)  #모집 제목
    join_count = models.IntegerField(default=1)  #모집 인원
    join_nowcount = models.IntegerField(default=0)  #현재 모집이 수락된 인원
    join_hits = models.PositiveIntegerField(default=0) #조회수
    join_desc = models.TextField()  #모집 설명
    join_period = models.DateField()  #모집 마감일
    join_status = models.BooleanField(default=True) # true일때 모집중, false 종료
    join_created_at = models.DateTimeField(auto_now_add=True) #모집 게시글 생성 시간
    join_updated_at = models.DateTimeField(auto_now= True) #모집 게시글 수정 시간
    

# 모집게시글 댓글 모델
class Comment(models.Model):
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE) # 댓글 작성자
    comment_article = models.ForeignKey(Join_Article, on_delete=models.CASCADE, related_name="comments") # 모집 게시글
    comment_content= models.TextField() # 댓글 내용
    comment_created_at = models.DateTimeField(auto_now_add=True) # 댓글 작성시간
    comment_updated_at = models.DateTimeField(auto_now= True) # 댓글 수정시간