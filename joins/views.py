from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from joins.models import Join_Article, Comment
from joins.serializers import JoinCommentCreateSerializer, JoinCommentSerializer, JoinSerializer, JoinCreateSerializer, JoinDetailSerializer


#모집 작성 및 불러오기 뷰(get, post)
class JoinArticleView(APIView):
    def get(self, request):
        join = Join_Article.objects.all().order_by("-join_created_at")
        serializer = JoinSerializer(join, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, festival_article_id):
        serializer = JoinCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(join_author_id=request.user.id, join_festival_id=festival_article_id)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 리뷰 상세보기/수정하기/삭제하기 뷰(get, patch, delete)
class JoinArticleDetailView(APIView):
    def get(self, request, join_id):
        joinview = get_object_or_404(Join_Article, id=join_id)
        joinview.join_hits = joinview.join_hits +1
        joinview.save()
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


# 댓글 전체 불러오기, 작성하기 뷰(get, post)
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


# 댓글 수정하기, 삭제하기 뷰(put, delete)
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