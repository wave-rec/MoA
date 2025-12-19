from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user_name', 'created_at']

class PostListSerializer(serializers.ModelSerializer):
    comment_count = serializers.IntegerField(read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'category',
            'user_name',
            'comment_count',
            'created_at',
        ]


class PostDetailSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('user',)
