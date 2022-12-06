from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from articles.models import Festival_Article, Comment, Bookmark
import random

# Create your views here.
class RecommendView(APIView):
    def get(self, request):
        userid = request.user  #현재 사용자
        print(userid)
        userregion = userid.user_address  #사용자의 주소(선호지역?)
        print(userregion)
        festivals = Festival_Article.objects.all().filter(festival_region__contains=userregion)  #추천받고 싶은 지역 기준                                           
        recommend_list = []
        nums = random.sample(range(0, len(festivals)), 5)  # 랜덤한 5개 숫자 뽑기
        for i in range(5):
            recommend_list.append(festivals[nums[i]])
        print(recommend_list)
        
class BookmarkView(APIView):
    def post(self, request, article_id):
        #현재 사용자
        user = request.user.id
        #축제게시물 가져오기
        article = get_object_or_404(Festival_Article, id=article_id)
        #현재 사용자와 해당 축제게시물에 대한 Bookmark db 보기
        bookmark = Bookmark.objects.filter(bookmark_user=user, bookmark_festival=article)
        # 존재한다면
        if bookmark.exists():
            bookmark.delete()  # 삭제하고
            return Response({"message": "북마크가 취소되었습니다"}, status=status.HTTP_204_NO_CONTENT)
        
        Bookmark.objects.create(
            bookmark_user = request.user,
            bookmark_festival = article
        )
        return Response({"message": "북마크가 되었습니다"}, status=status.HTTP_200_OK)