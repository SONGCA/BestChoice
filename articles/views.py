from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from articles.models import Festival_Article, Bookmark
import random

from articles.serializers import ArticleListSerializer, ArticleFilterSerializer

# Create your views here.
#추천축제게시글 불러오는 뷰
class RecommendView(APIView):
    def get(self, request):
        userid = request.user  #현재 사용자
        print(userid)
        userregion = userid.user_address  #사용자의 주소(선호지역? 경기도)
        print(userregion)
        festivals = Festival_Article.objects.all().filter(festival_region__contains=userregion)  #추천받고 싶은 지역 기준                                           
        recommend_list = []
        nums = random.sample(range(0, len(festivals)), 8)  # 랜덤한 8개 숫자 뽑기
        for i in range(8):
            recommend_list.append(festivals[nums[i]])
        
        serializer = ArticleListSerializer(recommend_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#전체축제게시글 불러오는 뷰
class CheckView(APIView):
    # authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        articles = Festival_Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

region_arr = ["서울시", "부산시", "대구시", "인천시", "광주시", "대전시", "울산시", "세종시", "경기도", "강원도", "충청북도", "충청남도", "전라북도", "전라남도", "경상북도", "경상남도", "제주도"]
    
#축제게시글 필터링해 불러오는 뷰    
class OptionView(APIView):
    def get(self, request):
        
        #url의 param 값을 저장
        param = request.query_params.getlist("param")
        
        #만약 url에 온 값이 없다면
        if not param:
            return Response({})

        region_list, cost_list, name = [], [], ""

        for p in param:
            print(p)
            if p in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17"]:  #value에 일치하는 지역명으로 변환 필요
                print(3)
                region = region_arr[int(p)-1]
                print(region)
                region_list.append(region)
                print(region_list)
            else:
                if "료" == p[-1]:
                    print(1)
                    cost_list.append(p)
                else:
                    print(2)
                    name += p
                    
        try:
            if len(region_list) > 0 and len(cost_list) > 0:
                print(12)
                results = Festival_Article.objects.filter(festival_region__contains=region_list[0]).filter(festival_cost__in=cost_list).distinct()
                for i in range(1, len(region_list)):
                    results = results.union(Festival_Article.objects.filter(festival_region__contains=region_list[i]).filter(festival_cost__in=cost_list).distinct())
                print(results)
            elif len(region_list) > 0:
                print(13)
                results = Festival_Article.objects.filter(festival_region__contains=region_list[0]).distinct()
                for i in range(1, len(region_list)):
                    results = results.union(Festival_Article.objects.filter(festival_region__contains=region_list[i]).distinct())
                print(results)
            elif len(cost_list) > 0:
                print(14)
                results = Festival_Article.objects.filter(festival_cost__in=cost_list).distinct()
            else:
                print(15)
                results = Festival_Article.objects.filter(festival_title__contains=name)

            if not results.exists():
                return Response({"message": "축제를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
            elif results.exists():
                serializer = ArticleFilterSerializer(results, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except:
            return Response({"message": "축제를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
    
#축제게시글 북마크하는 뷰
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