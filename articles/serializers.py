from turtle import update
from rest_framework import serializers
from articles.models import Festival_Article

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