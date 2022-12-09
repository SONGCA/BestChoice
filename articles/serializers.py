from turtle import update
from rest_framework import serializers
from articles.models import Festival_Article, Review, Review_Comment

# 게시글 리스트 serial
class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Festival_Article
        fields = ("pk", "festival_title", "festival_image", "festival_region")
        
# 게시글 필터링 serial
class ArticleFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Festival_Article
        fields = ("pk", "festival_title", "festival_image", "festival_region", "festival_cost")

# 리뷰 리스트 serial
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

# 리뷰 작성, 수정 serial
class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("review_title", "review_desc")

# 댓글 리스트 serial
class ReviewCommentSerializer(serializers.ModelSerializer):
    review_user = serializers.SerializerMethodField()

    def get_review_user(self, obj):
        return obj.review_user.user_nickname

    class Meta:
        model = Review_Comment
        fields = '__all__'

# 댓글 수정하기 serial
class ReviewCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review_Comment
        fields= ("review_comment",)