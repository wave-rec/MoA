from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'name', 'age')

    def create(self, validated_data):
        user = User.objects.create_user(
        username=validated_data['email'],
        email=validated_data['email'],
        password=validated_data['password'],
        name=validated_data.get('name'),
        age=validated_data.get('age'),
        )
        return user




class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(
            email=data['email'],
            password=data['password']
        )
        if not user:
            raise serializers.ValidationError('이메일 또는 비밀번호가 틀렸습니다.')
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'age')
