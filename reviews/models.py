from django.db import models
from users.models import User

# 리뷰 게시글
class Review(models.Model):
    review_author = models.ForeignKey(User, verbose_name="작성자", on_delete=models.CASCADE)  #리뷰 작성자
    review_title = models.CharField(max_length=20)  #리뷰 제목
    review_desc = models.TextField()  #리뷰 설명
    review_created_at = models.DateTimeField(auto_now_add=True) #리뷰 게시글 생성 시간
    review_updated_at = models.DateTimeField(auto_now= True) #리뷰 게시글 수정 시간
    image = models.ImageField(blank=False, null=True)   #리뷰 게시글 이미지
    count = models.PositiveIntegerField(default=0)  #리뷰 게시글 조회수

# 리뷰 게시글 댓글 모델
class Review_Comment(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE) # 리뷰 댓글 작성자
    review_article = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_comment') # 리뷰 모집 게시글
    review_comment= models.TextField() # 댓글 내용
    review_comment_created_at = models.DateTimeField(auto_now_add=True) # 댓글 작성시간
    review_comment_updated_at = models.DateTimeField(auto_now= True) # 댓글 수정시간