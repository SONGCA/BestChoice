from django.urls import path
from recruits import views


urlpatterns = [
    #신청게시글 관련(recruit article) -> request
    path('', views.RecruitArticleView.as_view(), name='recruit_view'),   #recruits/
    path('<int:join_id>/recruit/', views.RecruitArticleView.as_view(), name='recruit_view'),   #recruits/1(join id)/recruit/
    path('recruit/<int:recruit_id>/', views.RecruitDetailView.as_view(), name='recruit_detail_view'),   #recruits/recruit/2(recruit id)
    path('recruited/', views.RecruitedArticleView.as_view(), name='recruited_view'),   #recruits/recruited/
    path('recruited/<int:recruit_id>/<int:recruit_status>/', views.RecruitedChangeArticleView.as_view(), name='recruit_change_view'),   #recruits/recruited/1(recruit id)/1(recruit status)/
]