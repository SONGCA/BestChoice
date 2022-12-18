from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from reviews.models import Review, Review_Comment
from reviews.serializers import ReviewCommentSerializer, ReviewSerializer, ReviewCreateSerializer, ReviewCommentCreateSerializer


#리뷰 작성 및 불러오기 뷰(get, post)
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


# 리뷰 상세보기/수정하기/삭제하기 뷰(get, patch, delete)
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


# 댓글 전체 불러오기, 작성하기 뷰(get, post)
class ReviewCommentView(APIView):
    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        comments = review.review_comment.all()
        serializer = ReviewCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, review_id):
        serializer = ReviewCommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(review_user=request.user, review_article_id=review_id)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 댓글 수정하기, 삭제하기 뷰(put, delete)
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