from rest_framework import serializers
from festivals.models import Festival_Article, Bookmark

# 축제게시글 리스트 serial
class FestivalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Festival_Article
        fields = ("pk", "festival_title", "festival_desc", "festival_image", "festival_region")

# 축제게시글 북마크 serial        
class BookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ("pk", "bookmark_user", "bookmark_festival")

# 축제게시글 상세보기 serial
class FestivalSerializer(serializers.ModelSerializer): 
    bookmarks = BookMarkSerializer(many=True, read_only=True, source="bookmark_set")
    
    class Meta:
        model = Festival_Article
        fields = ("pk", "festival_title", "festival_desc", "festival_image", "festival_region", "festival_cost", "festival_address", "festival_start", "festival_end", "bookmarks")