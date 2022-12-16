from rest_framework import serializers
from recruits.models import Recruit_Article


class RecruitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruit_Article
        fields = "__all__"