from django.urls import path
from articles import views

urlpatterns = [
    path('festival/', views.RecommendView.as_view(), name='recommend_view'),
    path('festival/<int:festival_id>/bookmark/', views.BookmarkView.as_view(), name='bookmark_view'),
    path('check/', views.CheckView.as_view(), name='check_view'),
    path('filter/', views.OptionView.as_view(), name='filter_view')
]