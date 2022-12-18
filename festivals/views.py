from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from festivals.models import Festival_Article, Bookmark
import random


from festivals.serializers import FestivalListSerializer, FestivalSerializer, BookMarkSerializer
userregion_arr = [""]
region_arr = ["서울시", "부산시", "대구시", "인천시", "광주시", "대전시", "울산시", "세종시", "경기도", "강원도", "충청북도", "충청남도", "전라북도", "전라남도", "경상북도", "경상남도", "제주도"]


#추천축제게시글 불러오는 뷰(get)
class RecommendView(APIView):
    def get(self, request):
        userid = request.user  #현재 사용자
        userregion = userid.user_address  #사용자의 주소(선호지역? 경기도)
        festivals = Festival_Article.objects.all().filter(festival_region__contains=region_arr[int(userregion)-1])  #추천받고 싶은 지역 기준                                           
        recommend_list = []
        nums = random.sample(range(0, len(festivals)), 8)  # 랜덤한 8개 숫자 뽑기
        for i in range(8):
            recommend_list.append(festivals[nums[i]])
        
        serializer = FestivalListSerializer(recommend_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#전체 축제게시글 불러오는 뷰(get)
class FestivalListView(APIView):
    # authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        articles = Festival_Article.objects.all()
        serializer = FestivalListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
#축제게시글 필터링해 불러오는 뷰(get)   
class FestivalFilterView(APIView):
    def get(self, request):
        
        #url의 param 값을 저장
        param = request.query_params.getlist("param")
        
        #만약 url에 온 값이 없다면
        if not param:
            return Response({})

        region_list = []
        key_word = ""
        second_word = ""
        
        #검색창에서 입력 처리
        if len(param) == 2:
            key_word = param[0]
            second_word = param[1]
            
            if key_word == 'A':
                results = Festival_Article.objects.filter(festival_title__contains=second_word).distinct()
            elif key_word == 'T':
                results = Festival_Article.objects.filter(festival_desc__contains=second_word).distinct()
            elif key_word == 'C':
                results = Festival_Article.objects.filter(festival_cost__contains=second_word).distinct()
        
        #지역선택 처리
        for p in param:
            if p in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17"]:  #value에 일치하는 지역명으로 변환 필요
                region = region_arr[int(p)-1]
                region_list.append(region)
                    
        try:
            if len(region_list) > 0:
                results = Festival_Article.objects.filter(festival_region__contains=region_list[0]).distinct()
                for i in range(1, len(region_list)):
                    results = results.union(Festival_Article.objects.filter(festival_region__contains=region_list[i]).distinct())
           
            if not results.exists():
                return Response({"message": "축제를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
            elif results.exists():
                serializer = FestivalListSerializer(results, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except:
            return Response({"message": "축제를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)


# 축제게시글 상세보기 뷰(get)
class FestivalDetailView(APIView):
    def get(self, request, festival_article_id):
        festival = get_object_or_404(Festival_Article, id=festival_article_id)
        serializer = FestivalSerializer(festival)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
# 축제게시글 북마크 뷰(post)
class BookmarkView(APIView):
    def post(self, request, festival_article_id):
        #현재사용자 객체
        user = request.user.id
        #현재축제게시글 객체
        article = get_object_or_404(Festival_Article, id=festival_article_id)
        
        #현재 사용자와 해당 축제게시물에 대한 Bookmark db 보기
        bookmark = Bookmark.objects.filter(bookmark_user_id=user, bookmark_festival_id=article.id)
    
        # 존재한다면
        if bookmark.exists():
            bookmark.delete()  # 삭제하고
            return Response({"message": "북마크가 취소되었습니다"}, status=status.HTTP_204_NO_CONTENT)
        else:
            Bookmark.objects.create(bookmark_user_id=user, bookmark_festival_id = article.id)
            return Response({"message": "북마크가 되었습니다"}, status=status.HTTP_200_OK)