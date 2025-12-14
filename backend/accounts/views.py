from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    SignupSerializer,
    LoginSerializer,
    UserSerializer,
)
from .models import User


# 회원가입
@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': '회원가입 성공'}, status=201)
    return Response(serializer.errors, status=400)


# 로그인
@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)

        return Response({
            'access_token': str(refresh.access_token),
            'user': UserSerializer(user).data
        })
    return Response(serializer.errors, status=400)

# 내정보조회 및 수정
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user

    if request.method == 'GET':
        return Response(UserSerializer(user).data)

    if request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


# 로그이웃
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    return Response({'message': '로그아웃 완료'})

# 회원탈퇴
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def withdraw(request):
    request.user.delete()
    return Response({'message': '회원탈퇴 완료'}, status=204)

