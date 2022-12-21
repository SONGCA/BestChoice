from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from users.models import User
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer, UserProfileSerializer, UserEditSerializer

# 회원가입 view


class UserView(APIView):
    def post(self, request):
        if User.objects.filter(email = request.data["email"]):
            return Response({"message" : "이미 가입된 이메일입니다. "}, status=status.HTTP_400_BAD_REQUEST)
        
        elif User.objects.filter(user_nickname = request.data["user_nickname"]):
            return Response({"message" : "중복된 닉네임입니다. "}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"회원가입이 정상적으로 완료되었습니다!"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    #프로필 정보 불러오기
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    
    #프로필 정보 수정하기
    def patch(self, request):
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserEditSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer