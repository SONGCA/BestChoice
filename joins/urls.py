from django.urls import path
from joins import views

urlpatterns = [
    #모집게시글 관련(join article)
    path('<int:festival_article_id>/createjoin/', views.JoinArticleView.as_view(), name='join_view'),   #joins/1(festival id)/createjoin/
    path('', views.JoinArticleView.as_view(), name='join_list_view'),   #joins/
    path('<int:join_id>/', views.JoinArticleDetailView.as_view(), name='join_detail_view'),   #joins/1(join id)
    path('<int:join_id>/comment/', views.JoinCommentView.as_view(), name='join_comment_view'),   #joins/1(join id)/comment
    path('<int:join_id>/comment/<int:join_comment_id>/', views.JoinCommentDetailView.as_view(), name='join_comment_detail_view'),   #joins/1(join id)/comment/2(join comment id)/
]