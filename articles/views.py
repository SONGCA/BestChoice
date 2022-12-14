from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from articles.models import Festival_Article, Bookmark, Review, Review_Comment
from users.models import User
import random


from articles.serializers import FestivalListSerializer, FestivalSerializer, ReviewSerializer, ReviewCreateSerializer, ReviewCommentSerializer, ReviewCommentCreateSerializer, BookMarkSerializer

userregion_arr = [""]
region_arr = ["서울시", "부산시", "대구시", "인천시", "광주시", "대전시", "울산시", "세종시", "경기도", "강원도", "충청북도", "충청남도", "전라북도", "전라남도", "경상북도", "경상남도", "제주도"]

# Create your views here.
#추천축제게시글 불러오는 뷰
class RecommendView(APIView):
    def get(self, request):
        userid = request.user  #현재 사용자
        print(userid)
        userregion = userid.user_address  #사용자의 주소(선호지역? 경기도)
        print(userregion)
        festivals = Festival_Article.objects.all().filter(festival_region__contains=region_arr[int(userregion)-1])  #추천받고 싶은 지역 기준                                           
        recommend_list = []
        nums = random.sample(range(0, len(festivals)), 8)  # 랜덤한 8개 숫자 뽑기
        for i in range(8):
            recommend_list.append(festivals[nums[i]])
        
        serializer = FestivalListSerializer(recommend_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#전체 축제게시글 불러오는 뷰
class FestivalListView(APIView):
    # authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        articles = Festival_Article.objects.all()
        serializer = FestivalListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
#축제게시글 필터링해 불러오는 뷰    
class FestivalFilterView(APIView):
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
                serializer = FestivalListSerializer(results, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except:
            return Response({"message": "축제를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

# 축제 상세 페이지 뷰
class FestivalDetailView(APIView):
    def get(self, request, festival_article_id):
        festival = get_object_or_404(Festival_Article, id=festival_article_id)
        serializer = FestivalSerializer(festival)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# 축제게시글 북마크 뷰
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

#리뷰 작성 및 불러오기
class ReviewView(APIView):
    def get(self, request):
        review = Review.objects.all().order_by("-review_created_at")
        serializer = ReviewSerializer(review, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(review_author=request.user)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 리뷰 상세보기/수정하기/삭제하기
class ReviewDetailView(APIView):
    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        review.count = review.count + 1
        review.save()
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        # 요청자가 게시글 작성자일 경우에만 수정 가능
        if request.user == review.review_author:
            serializer = ReviewCreateSerializer(review, data=request.data)
            if serializer.is_valid():
                serializer.save()  # 수정이기 때문에 user정보 불필요
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        if request.user == review.review_author:
            review.delete()
            return Response("삭제되었습니다.", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)


# 댓글 전체 불러오기, 작성하기
class ReviewCommentView(APIView):
    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        comments = review.review_comment_set.all()
        serializer = ReviewCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, review_id):
        serializer = ReviewCommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(review_user=request.user, review_article_id=review_id)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 댓글 수정하기, 삭제하기
class ReviewCommentDetailView(APIView):
    def put(self, request, review_id, comment_id):
        review_comment = get_object_or_404(Review_Comment, id=comment_id)
        if request.user == review_comment.review_user:
            serializer = ReviewCommentCreateSerializer(review_comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, review_id, comment_id):
        review_comment = get_object_or_404(Review_Comment, id=comment_id)
        if request.user == review_comment.review_user:
            review_comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)
