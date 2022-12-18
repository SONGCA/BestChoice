from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from recruits.models import Join_Article, Recruit_Article
from recruits.serializers import RecruitSerializer
import random


# 신청게시글 조회 뷰(get, post)
class RecruitArticleView(APIView):
    # 본인이 작성한(recruit_user_id가 사용자인) recruit 게시글 상태보기 -> 내가 신청한 내역을 보기 위해
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
        
        #현재 사용자와 해당 축제게시물에 대한 Bookmark db 보기
        recruit = Recruit_Article.objects.filter(recruit_user_id=user, recruit_join_id=join_id)
    
        # 존재한다면
        if recruit.exists():
            return Response({"message": "이미 해당 모집글에 신청되었습니다."}, status=status.HTTP_302_FOUND)
        else:
            Recruit_Article.objects.create(recruit_user_id=user, recruit_join_id=join_id)
            return Response({"message": "해당 모집글에 신청되었습니다."}, status=status.HTTP_201_CREATED)
 
 
# 특정 신청게시글 조회 뷰(get)       
class RecruitDetailView(APIView):
    def get(self, request, recruit_id):
        recruit = get_object_or_404(Recruit_Article, id=recruit_id)
        serializer = RecruitSerializer(recruit)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

# 본인이 작성한 모집게시글에 대한 신청 내역 조회하기(get)
class RecruitedArticleView(APIView):
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
            results = Recruit_Article.objects.filter(recruit_join_id=myjoins_list[0]).exclude(recruit_status=2).distinct()
            for j in range(1, len(myjoins_list)):
                results = results.union(Recruit_Article.objects.filter(recruit_join_id=myjoins_list[j]).exclude(recruit_status=2).distinct())
                                        
            if not results.exists():
                    return Response({"message": "작성한 모집글에 대한 신청게시글을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
            elif results.exists():
                    serializer = RecruitSerializer(results, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "작성한 모집글에 대한 신청게시글을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)


# 신청게시글 상태를 변경하는 뷰(patch)
class RecruitedChangeArticleView(APIView):          
    # 본인이 작성한 모집게시글에 대한 신청 내역 상태 변경하기        
    def patch(self, request, recruit_id, recruit_status):
        recruitpatch = get_object_or_404(Recruit_Article, id=recruit_id)  
        print(recruitpatch)
        #"id": 3,
        #"recruit_status": 0,
        #"recruit_time": "2022-12-13T11:22:50.661067+09:00",
        #"recruit_user": 1,
        #"recruit_join": 3
        myjoin = get_object_or_404(Join_Article, id=recruitpatch.recruit_join.id)  #신청게시글에 적혀있는 모집게시물
        print(myjoin)
        # 요청자가 게시글 작성자일 경우에만 수정 가능
        if request.user == myjoin.join_author:  #신청게시글에 적혀있는 모집게시글의 작성자가 현재사용자라면
            if recruit_status == 1:
                recruitpatch.recruit_status = 1
                recruitpatch.save()
                return Response("신청상태가 수락으로 변경되었습니다.", status=status.HTTP_200_OK)
            elif recruit_status == 2:
                recruitpatch.recruit_status = 2
                recruitpatch.save()
                return Response("신청상태가 거절로 변경되었습니다.", status=status.HTTP_200_OK)
            else:
                return Response("상태변경을 할 수 없습니다.", status=status.HTTP_403_FORBIDDEN)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_401_UNAUTHORIZED)