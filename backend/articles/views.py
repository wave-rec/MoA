from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    CommentSerializer,
)
from .permissions import IsOwner
from django.db.models import Count

# 게시글 목록 및 작성
class PostListCreateView(generics.ListCreateAPIView):
    permission_classes = []

    def get_queryset(self):
        queryset = Post.objects.annotate(
            comment_count=Count('comments')
        ).order_by('-created_at')

        category = self.request.query_params.get('category')
        if category:
            category = category.rstrip('/') 
            queryset = queryset.filter(category=category)

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostListSerializer
        return PostDetailSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return []



# 게시글 상세, 수정, 삭제
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), IsOwner()]
        return []


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
