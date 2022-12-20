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
        recruit = Recruit_Article.objects.filter(recruit_user_id=user).order_by("-recruit_time")
        serializer = RecruitSerializer(recruit, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    # 신청게시글 생성 메서드
    def post(self, request, join_id):
        #현재사용자 객체
        user = request.user.id
        #현재축제게시글 객체
        
        #현재사용자, 모집게시글 아이디를 이용해 recruit article 뽑아내기
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
        # myjoin_list = [1, 6, 8] 이런식으로....
        for i in range(len(myjoins)):
            myjoins_list.append(myjoins[i].id)
        #myjoins의 join id와 Recruit_Article의 recruit_join이 일치하는
        #예를들어 join id가 1인 Recruit_Article 찾고, join id가 2인 Recruit_Article 찬고 이런 식으로...,
        
        
        if len(myjoins_list) > 0:
            results = Recruit_Article.objects.filter(recruit_join_id=myjoins_list[0]).distinct()
    
            for j in range(1, len(myjoins_list)):
                results = results.union(Recruit_Article.objects.filter(recruit_join_id=myjoins_list[j]).distinct())
                                        
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
        recruitpatch = get_object_or_404(Recruit_Article, id=recruit_id) #상태변경을 하고자 하는 신청게시글 객체 불러오기 
        # recruitpatch 예시
        #"id": 3,
        #"recruit_status": 0,
        #"recruit_time": "2022-12-13T11:22:50.661067+09:00",
        #"recruit_user": 1,
        #"recruit_join": 3
        myjoin = get_object_or_404(Join_Article, id=recruitpatch.recruit_join.id)  #신청게시글에 적혀있는 모집게시글 객체 불러오기
        myjoin_recruits = Recruit_Article.objects.filter(recruit_join_id=myjoin.id)  #상태변경을 원하는 신청게시글의 모집게시글 번호에 달린 모든 신청게시글 객체 불러오기
        if myjoin.join_status == False:  #모집게시글이 마감된 경우
            if recruitpatch.recruit_status==1 and recruit_status==1:  #현재신청이 수락인데 수락으로 변경하고자 할 때
                return Response({"message": "이미 수락되었습니다."}, status=status.HTTP_202_ACCEPTED)
            elif recruitpatch.recruit_status==2 and recruit_status==1:  #현재신청이 거절인데 수락으로 변경하고자 할 때
                return Response({"message": "모집인원을 초과합니다."}, status=status.HTTP_202_ACCEPTED)
            elif recruitpatch.recruit_status==1 and recruit_status==2:  #현재신청이 수락인데 거절로 변경하고자 할 때
                recruitpatch.recruit_status = 2  #신청게시글을 거절상태로 변경하고
                recruitpatch.save()  #저장하고
                myjoin.join_nowcount -= 1  #모집게시글의 현재 참여인원수를 1감소하고
                myjoin.join_status = True  #모집가능 상태로 변경하고
                myjoin.save()  #저장
                return Response({"message": "신청상태가 거절로 변경되었습니다."}, status=status.HTTP_200_OK)
            elif recruitpatch.recruit_status==2 and recruit_status==2:  #현재신청이 거절인데 거절로 변경하고자 할 때
                return Response({"message": "이미 거절되었습니다."}, status=status.HTTP_202_ACCEPTED)
            else:  #모집마감 시 미정이 모두 거절로 변경되지만 혹시 모르니까
                return Response({"message":"모집인원이 마감되었습니다."}, status=status.HTTP_202_ACCEPTED)
        else:  #모집게시글이 진행중일 경우
            # 요청자가 게시글 작성자일 경우에만 수정 가능
            if request.user == myjoin.join_author:  #신청게시글에 적혀있는 모집게시글의 작성자가 현재사용자라면
                if recruit_status == 1:  #수락으로 변경하고자 할 때(버튼)
                    recruitpatch.recruit_status = 1  #신청게시글 상태를 수락으로 변경하고 저장
                    recruitpatch.save()
                    myjoin.join_nowcount += 1  #모집게시글의 현재 참여 인원을 1증가 시키고 저장
                    myjoin.save()
                    if myjoin.join_nowcount == myjoin.join_count:  #방금의 변화로 현재 인원이 정원과 같은지 확인
                        myjoin.join_status = False  #같으면 모집게시글 상태를 마감으로 변경하고 저장
                        myjoin.save()
                        for recruit_obj in myjoin_recruits:  #해당 모집게시글에 달린 모든 신청게시글에 대해
                            if recruit_obj.recruit_status == 0:  #미정 상태는 모두 거절로 변경하고 저장
                                recruit_obj.recruit_status = 2
                                recruit_obj.save()
                    return Response({"message": "신청상태가 수락으로 변경되었습니다."}, status=status.HTTP_200_OK)
                elif recruit_status == 2:  #거절로 변경하고자 할 때(버튼)
                    recruitpatch.recruit_status = 2  #신청게시글 상태를 거절로 변경하고 저장
                    recruitpatch.save()
                    return Response({"message": "신청상태가 거절로 변경되었습니다."}, status=status.HTTP_200_OK)
                else:  # 수락 or 거절 이외의 값 -> 혹시 모르니까
                    return Response({"message": "상태변경을 할 수 없습니다."}, status=status.HTTP_403_FORBIDDEN)
            else:  # 상태변화 권한이 없는 경우
                return Response({"message": "권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)