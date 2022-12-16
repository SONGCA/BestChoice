from django.urls import path
from festivals import views

urlpatterns = [
    #축제게시글 관련(festival article)
    path('', views.FestivalListView.as_view(), name='festival_list_view'),   #festivals/
    path('recommend/', views.RecommendView.as_view(), name='recommend_view'),   #festivals/recommend/
    path('filter/', views.FestivalFilterView.as_view(), name='festival_filter_view'),  #festivals/filter/
    path('<int:festival_article_id>/', views.FestivalDetailView.as_view(), name='festival_detail_view'),   #festivals/1/
    path('<int:festival_article_id>/bookmark/', views.BookmarkView.as_view(), name='bookmark_view'),   #festivals/1/bookmark/
]