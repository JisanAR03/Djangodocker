from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import FrontendContent

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'password', 'email', 'user_type']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=validated_data['user_type']
        )
        return user

class FrontendContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrontendContent
        fields = ['id','content_type', 'title_type', 'image', 'author', 'content', 'created_at']
        extra_kwargs = {'author': {'read_only': True}}
        
    def create(self, validated_data):
        user = self.context['request'].user
        frontend_content = FrontendContent.objects.create(
            content_type=validated_data['content_type'],
            title_type=validated_data['title_type'],
            image=validated_data['image'],
            author=user,
            content=validated_data['content']
        )
        return frontend_content
    
    def update(self, instance, validated_data):
        instance.content_type = validated_data.get('content_type', instance.content_type)
        instance.title_type = validated_data.get('title_type', instance.title_type)
        instance.image = validated_data.get('image', instance.image)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance