from rest_framework import serializers
from reviews.models import Review, Review_Comment


# 리뷰 댓글 리스트 serial
class ReviewCommentSerializer(serializers.ModelSerializer):
    review_user = serializers.SerializerMethodField()
    
    def get_review_user(self, obj):
        return obj.review_user.user_nickname
    
    class Meta:
        model = Review_Comment
        fields = '__all__'

        
# 리뷰 댓글 작성 serial
class ReviewCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review_Comment
        fields= ("review_comment",)
        
        
# 리뷰 리스트 serial
class ReviewSerializer(serializers.ModelSerializer):
    review_author = serializers.SerializerMethodField()
    review_comment = ReviewCommentSerializer(many=True)
    
    def get_review_author(self, obj):
        return obj.review_author.user_nickname
    
    class Meta:
        model = Review
        fields = '__all__'
        
        
# 리뷰 작성, 수정 serial
class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("review_title", "review_desc", 'image')