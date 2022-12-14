from django.urls import path
from articles import views

urlpatterns = [
    path('recommend/', views.RecommendView.as_view(), name='recommend_view'),
    path('festival/', views.FestivalListView.as_view(), name='festival_list_view'),
    path('festival/filter/', views.FestivalFilterView.as_view(), name='festival_filter_view'),
    path('festival/<int:festival_article_id>/', views.FestivalDetailView.as_view(), name='festival_detail_view'),
    path('festival/<int:festival_article_id>/bookmark/', views.BookmarkView.as_view(), name='bookmark_view'),
    path('festival/<int:festival_article_id>/createjoin/', views.JoinArticleCreate.as_view(), name='join_create'),
    path('festival/join/', views.JoinArticleCreate.as_view(), name='join_list_view'),
    path('festival/join/<int:join_id>/', views.JoinArticleDetailView.as_view(), name='join_detail_view'),
    path('festival/join/<int:join_id>/recruit/', views.RecruitArticleView.as_view(), name='recruit_view'),
    path('festival/join/recruit/', views.RecruitArticleView.as_view(), name='recruit_view'),  # 추후에 url 변경 필요
    path('festival/join/recruit/<int:recruit_id>/', views.RecruitDetailView.as_view(), name='recruit_detail_view'), # 추후에 url 변경 필요
    path('festival/join/recruited/', views.RecruitedArticleView.as_view(), name='recruited_view'),  # 추후에 url 변경 필요
    path('festival/join/recruited/<int:recruit_id>/<int:recruit_status>/', views.RecruitedChangeArticleView.as_view(), name='recruit_change_view'),  # 추후에 url 변경 필요  # 추후에 url 변경 필요
    path('festival/join/<int:join_id>/comment/', views.JoinCommentView.as_view(), name='join_comment_view'),
    path('festival/join/<int:join_id>/comment/<int:join_comment_id>/', views.JoinCommentDetailView.as_view(), name='join_comment_detail_view'),
    path('review/', views.ReviewView.as_view(), name='review_view'),
    path('review/<int:review_id>/', views.ReviewDetailView.as_view(), name='review_detail_view'),
    path('review/<int:review_id>/comment/', views.ReviewCommentView.as_view(), name='reveiw_comment_view'),
    path('review/<int:review_id>/comment/<int:review_comment_id>/', views.ReviewCommentDetailView.as_view(), name='review_comment_detail_view'),
]