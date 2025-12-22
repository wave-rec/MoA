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
from products.models import Product
from products.serializers import ProductListSerializer


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

# 찜 관련
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_favorites(request):
    qs = (
        Product.objects
        .filter(favorite_by__user=request.user)
        .distinct()
        .order_by("-favorite_by__created_at")
    )
    serializer = ProductListSerializer(qs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 비밀번호 변경
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user

    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')

    if not current_password or not new_password:
        return Response(
            {'detail': '현재 비밀번호와 새 비밀번호를 모두 입력해주세요.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 현재 비밀번호 검증
    if not user.check_password(current_password):
        return Response(
            {'detail': '현재 비밀번호가 올바르지 않습니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 새 비밀번호 저장
    user.set_password(new_password)
    user.save()

    return Response(
        {'detail': '비밀번호가 변경되었습니다.'},
        status=status.HTTP_200_OK
    )
