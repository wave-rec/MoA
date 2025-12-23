from rest_framework import serializers
from .models import Post, Comment, PostImage


class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user_name', 'user_id', 'created_at']


class PostListSerializer(serializers.ModelSerializer):
    comment_count = serializers.IntegerField(read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)

    category_display = serializers.CharField(
        source='get_category_display',
        read_only=True
    )
    
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'category',
            'user_name',
            'comment_count',
            'created_at',
            'category_display',
        ]

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'image']


class PostDetailSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    images = PostImageSerializer(many=True, read_only=True)

    category_display = serializers.CharField(
        source='get_category_display',
        read_only=True
    )

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('user',)
