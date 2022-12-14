from rest_framework import serializers
from articles.models import Festival_Article, Review, Review_Comment, Bookmark

# 축제 리스트 serial
class FestivalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Festival_Article
        fields = ("pk", "festival_title", "festival_desc", "festival_image", "festival_region")
    
# 축제 상세페이지 serial
class FestivalSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Festival_Article
        fields = '__all__'

# 게시글 북마크 serial        
class BookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ("pk", "bookmark_user", "bookmark_festival")

# 리뷰 댓글 리스트 serial
class ReviewCommentSerializer(serializers.ModelSerializer):
    review_user = serializers.SerializerMethodField()

    def get_review_user(self, obj):
        return obj.review_user.user_nickname

    class Meta:
        model = Review_Comment
        fields = '__all__'

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


# 리뷰 댓글 작성 serial
class ReviewCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review_Comment
        fields= ("review_comment",)