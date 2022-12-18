from django.urls import path
from reviews import views

urlpatterns = [
     #리뷰게시글 관련(review article)
    path('', views.ReviewView.as_view(), name='review_view'),   #reviews/
    path('<int:review_id>/', views.ReviewDetailView.as_view(), name='review_detail_view'),   #reviews/1/
    path('<int:review_id>/comment/', views.ReviewCommentView.as_view(), name='reveiw_comment_view'),   #reviews/1/comment/
    path('<int:review_id>/comment/<int:review_comment_id>/', views.ReviewCommentDetailView.as_view(), name='review_comment_detail_view'),   #reviews/1/comment/2
]