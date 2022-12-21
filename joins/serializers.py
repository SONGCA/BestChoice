from rest_framework import serializers
from joins.models import Join_Article, Comment
from festivals.serializers import FestivalListSerializer
from recruits.serializers import RecruitSerializer


# 모집 댓글 리스트 serial
class JoinCommentSerializer(serializers.ModelSerializer):
    comment_user = serializers.SerializerMethodField()

    def get_comment_user(self, obj):
        return obj.comment_user.user_nickname
    class Meta:
        model = Comment
        fields = "__all__"


# 모집 댓글 작성 serial
class JoinCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("comment_content",)
        
        
# 모집 리스트 serial
class JoinSerializer(serializers.ModelSerializer):
    join_author = serializers.SerializerMethodField()
    join_festival = FestivalListSerializer()

    def get_join_author(self, obj):
        return obj.join_author.user_nickname

    def get_join_festival(self, obj):
        return obj.join_festival.festival_title
    class Meta:
        model = Join_Article
        fields = "__all__"
        
                
#모집게시글 생성/수정 serial
class JoinCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Join_Article
        fields = ("join_title", "join_count", "join_desc", "join_period",)
        
# 모집게시글 상세보기 serial
class JoinDetailSerializer(serializers.ModelSerializer):
    join_author = serializers.SerializerMethodField()
    join_festival = serializers.SerializerMethodField()
    comments = JoinCommentSerializer(many=True)
    recruit_join_set = RecruitSerializer(many=True)

    def get_join_author(self, obj):
        return obj.join_author.user_nickname

    def get_join_festival(self, obj):
        return obj.join_festival.festival_title
    
    class Meta:
        model = Join_Article
        fields = "__all__"