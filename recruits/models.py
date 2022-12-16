from django.db import models
from users.models import User
from joins.models import Join_Article


# 신청게시글 모델
class Recruit_Article(models.Model):
    recruit_user = models.ForeignKey(User, verbose_name="작성자", on_delete=models.CASCADE, related_name="recruit_user_set")  #신청게시글 작성자
    recruit_join = models.ForeignKey(Join_Article, verbose_name="모집", on_delete=models.CASCADE, related_name="recruit_join_set")  #신청게시글 해당 모집글
    recruit_status = models.IntegerField(default=0)   #0 : 미정 1 : 수락 2 : 거절
    recruit_time = models.DateTimeField(auto_now_add=True)  #신청게시글 생성시간