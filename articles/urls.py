from django.urls import path
from articles import views

urlpatterns = [
    path('recommend/', views.RecommendView.as_view(), name='recommend_view'),
    path('festival/', views.FestivalListView.as_view(), name='festival_list_view'),
    path('festival/filter/', views.FestivalFilterView.as_view(), name='festival_filter_view'),
    path('festival/<int:festival_article_id>/', views.FestivalDetailView.as_view(), name='festival_detail_view'),
    path('festival/<int:festival_article_id>/bookmark/', views.BookmarkView.as_view(), name='bookmark_view'),
    path('review/', views.ReviewView.as_view(), name='review_view'),
    path('review/<int:review_id>/', views.ReviewDetailView.as_view(), name='review_detail_view'),
    path('review/<int:review_id>/comment/', views.ReviewCommentView.as_view(), name='reveiw_comment_view'),
    path('review/<int:review_id>/comment/<int:comment_id>/', views.ReviewCommentDetailView.as_view(), name='review_comment_detail_view'),
]