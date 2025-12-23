from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Count, Q
from .models import Post, Comment, PostImage
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    CommentSerializer,
)
from .permissions import IsOwner
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

# 게시글 목록 및 작성
class PostListCreateView(generics.ListCreateAPIView):
    permission_classes = []
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        queryset = Post.objects.annotate(
            comment_count=Count('comments')
        ).order_by('-created_at')

        # 카테고리 필터
        category = self.request.query_params.get('category')
        if category:
            category = category.rstrip('/')
            queryset = queryset.filter(category=category)

        # 검색 필터 (제목 OR 내용)
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search)
            )
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostListSerializer
        return PostDetailSerializer

    def perform_create(self, serializer):
        post = serializer.save(user=self.request.user)

        images = self.request.FILES.getlist('images')
        for image in images:
            PostImage.objects.create(post=post, image=image)
            
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return []



# 게시글 상세, 수정, 삭제
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), IsOwner()]
        return []
    
    def perform_update(self, serializer):
        post = serializer.save()

        images = self.request.FILES.getlist('images')

        if images:
            # 기존 이미지 삭제
            PostImage.objects.filter(post=post).delete()

            # 새 이미지 저장
            for image in images:
                PostImage.objects.create(post=post, image=image)



# 댓글 목록, 작성
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    pagination_class = None

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            post_id=self.kwargs['post_id']
        )

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return []

# 댓글 수정, 삭제
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), IsOwner()]
        return []



class MyPostListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = (
            Post.objects
            .filter(user=request.user)
            .annotate(comment_count=Count('comments'))
            .order_by('-created_at')
        )
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)