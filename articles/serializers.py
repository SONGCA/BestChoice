from rest_framework import serializers
from articles.models import Festival_Article, Review, Review_Comment, Bookmark, Join_Article, Comment

# 축제 리스트 serial
class FestivalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Festival_Article
        fields = ("pk", "festival_title", "festival_desc", "festival_image", "festival_region")

# 게시글 북마크 serial        
class BookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ("pk", "bookmark_user", "bookmark_festival")

# 축제 상세페이지 serial
class FestivalSerializer(serializers.ModelSerializer): 
    bookmarks = BookMarkSerializer(many=True, read_only=True, source="bookmark_set")
    
    class Meta:
        model = Festival_Article
        fields = ("pk", "festival_title", "festival_desc", "festival_image", "festival_region", "festival_cost", "festival_address", "festival_start", "festival_end", "bookmarks")
                
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


#모집게시글 생성/수정 serial
class JoinCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Join_Article
        fields = ("join_title", "join_count", "join_desc", "join_period",)

class JoinListSerializer(serializers.ModelSerializer):
    join_author = serializers.SerializerMethodField()
    join_festival = FestivalListSerializer()

    def get_join_author(self, obj):
        return obj.join_author.user_nickname

    def get_join_festival(self, obj):
        return obj.join_festival.festival_title
    class Meta:
        model = Join_Article
        fields = "__all__"
        
class JoinCommentSerializer(serializers.ModelSerializer):
    comment_user = serializers.SerializerMethodField()

    def get_comment_user(self, obj):
        return obj.comment_user.user_nickname
    class Meta:
        model = Comment
        fields = "__all__"

class JoinCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("comment_content",)

class JoinDetailSerializer(serializers.ModelSerializer):
    join_author = serializers.SerializerMethodField()
    join_festival = serializers.SerializerMethodField()
    comments = JoinCommentSerializer(many=True)

    def get_join_author(self, obj):
        return obj.join_author.user_nickname

    def get_join_festival(self, obj):
        return obj.join_festival.festival_title
    
    class Meta:
        model = Join_Article
        fields = "__all__"




# class CommentSerializer(serializers.ModelSerializer):
#     user = serializers.SerializerMethodField()

#     def get_user(self, obj):
#         return obj.user.nickname
    
#     class Meta:
#         model = Comment
#         fields = '__all__'


# class ArticleSerializer(serializers.ModelSerializer):
#     user = serializers.SerializerMethodField()
#     comment_set = CommentSerializer(many=True)
    
#     def get_user(self, obj):
#         return obj.user.email
    
#     class Meta:
#         model = Article
#         fields = '__all__'