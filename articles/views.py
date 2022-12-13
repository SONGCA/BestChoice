from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from articles.models import Festival_Article, Bookmark, Review, Review_Comment, Join_Article, Comment, Recruit_Article
from users.models import User
import random


from articles.serializers import FestivalListSerializer, JoinDetailSerializer, JoinCommentCreateSerializer, JoinCommentSerializer, JoinListSerializer, FestivalSerializer, ReviewSerializer, ReviewCreateSerializer, ReviewCommentSerializer, ReviewCommentCreateSerializer, JoinCreateSerializer, BookMarkSerializer, RecruitSerializer
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
        review = Review.objects.all()
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
    def put(self, request, review_id, review_comment_id):
        review_comment = get_object_or_404(Review_Comment, id=review_comment_id)
        if request.user == review_comment.review_user:
            serializer = ReviewCommentCreateSerializer(review_comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, review_id, review_comment_id):
        review_comment = get_object_or_404(Review_Comment, id=review_comment_id)
        if request.user == review_comment.review_user:
            review_comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)

class JoinArticleCreate(APIView):
    def get(self, request):
        join = Join_Article.objects.all()
        serializer = JoinListSerializer(join, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, festival_article_id):
        serializer = JoinCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(join_author_id=request.user.id, join_festival_id=festival_article_id)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JoinArticleDetailView(APIView):
    def get(self, request, join_id):
        joinview = get_object_or_404(Join_Article, id=join_id)
        serializer = JoinDetailSerializer(joinview)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, join_id):
        joinpatch = get_object_or_404(Join_Article, id=join_id)
        # 요청자가 게시글 작성자일 경우에만 수정 가능
        if request.user == joinpatch.join_author:
            serializer = JoinCreateSerializer(joinpatch, data=request.data)
            if serializer.is_valid():
                serializer.save()  # 수정이기 때문에 user정보 불필요
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, join_id):
        joindelete = get_object_or_404(Join_Article, id=join_id)
        if request.user == joindelete.join_author:
            joindelete.delete()
            return Response("삭제되었습니다.", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)

class JoinCommentView(APIView):
    def get(self, request, join_id):
        joincomment = get_object_or_404(Join_Article, id=join_id)
        comments = joincomment.comments.all()
        serializer = JoinCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, join_id):
        serializer = JoinCommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(comment_user_id=request.user.id, comment_article_id=join_id)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JoinCommentDetailView(APIView):
    def put(self, request, join_id, join_comment_id):
        join_comment = get_object_or_404(Comment, id=join_comment_id)
        if request.user == join_comment.comment_user:
            serializer = JoinCommentCreateSerializer(join_comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, join_id, join_comment_id):
        join_comment = get_object_or_404(Comment, id=join_comment_id)
        if request.user == join_comment.comment_user:
            join_comment.delete()
            return Response("삭제되었습니다.", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)
        
        

# 신청게시글 
class RecruitArticleView(APIView):
    # 본인이 작성한(recruit_user_id가 사용자인) recruit 게시글 상태보기
    def get(self, request):
        user = request.user.id  #현재 사용자
        recruit = Recruit_Article.objects.filter(recruit_user_id=user)
        serializer = RecruitSerializer(recruit, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        
    # 신청게시글 생성 메서드
    def post(self, request, join_id):
        #현재사용자 객체
        user = request.user.id
        # #현재축제게시글 객체
        # joinarticle = get_object_or_404(Join_Article, id=join_id)
        
        #현재 사용자와 해당 축제게시물에 대한 Bookmark db 보기
        recruit = Recruit_Article.objects.filter(recruit_user_id=user, recruit_join_id=join_id)
    
        # 존재한다면
        if recruit.exists():
            return Response({"message": "이미 해당 모집글에 신청되었습니다."}, status=status.HTTP_302_FOUND)
        else:
            Recruit_Article.objects.create(recruit_user_id=user, recruit_join_id=join_id)
            return Response({"message": "해당 모집글에 신청되었습니다."}, status=status.HTTP_201_CREATED)
        
    
class RecruitedArticleView(APIView):
    
    # 본인이 작성한 모집게시글에 대한 신청 내역 조회하기
    def get(self, request):
        user = request.user.id
        myjoins_list = []
        myjoins = Join_Article.objects.filter(join_author_id=user)  #본인이 작성한 모집게시글들
        # myjoin_list = [1, 2] 이런식으로....
        for i in range(len(myjoins)):
            myjoins_list.append(myjoins[i].id)
        #myjoins의 join id와 Recruit_Article의 recruit_join이 일치하는
        #예를들어 join id가 1인 Recruit_Article 찾고, join id가 2인 Recruit_Article 찬고 이런 식으로...,
        
        if len(myjoins_list) > 0:
            results = Recruit_Article.objects.filter(recruit_join_id=myjoins_list[0])
            for j in range(1, len(myjoins_list)):
                results = results.union(Recruit_Article.objects.filter(recruit_join_id=myjoins_list[j]))
                                        
        if not results.exists():
                return Response({"message": "작성한 모집글에 대한 신청게시글을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        elif results.exists():
                serializer = RecruitSerializer(results, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK) 


class RecruitedChangeArticleView(APIView):          
    # 본인이 작성한 모집게시글에 대한 신청 내역 상태 변경하기        
    def patch(self, request, recruit_id):
        recruitpatch = get_object_or_404(Recruit_Article, id=recruit_id)  
        print(recruitpatch)
        #"id": 3,
        #"recruit_status": false,
        #"recruit_time": "2022-12-13T11:22:50.661067+09:00",
        #"recruit_user": 1,
        #"recruit_join": 3
        myjoin = get_object_or_404(Join_Article, id=recruitpatch.recruit_join.id)  #신청게시글에 적혀있는 모집게시물
        print(myjoin)
        # 요청자가 게시글 작성자일 경우에만 수정 가능
        if request.user == myjoin.join_author:  #신청게시글에 적혀있는 모집게시글의 작성자가 현재사용자라면
            recruitpatch.recruit_status = True
            recruitpatch.save()
            return Response("신청상태가 확정으로 변경되었습니다.", status=status.HTTP_200_OK)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)