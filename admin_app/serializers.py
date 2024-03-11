from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import FrontendContent, Menu, MenuContent, Contact_form
from django.conf import settings
from django.core.mail import send_mail

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'password', 'email', 'user_type', 'creator']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=validated_data['user_type'],
            creator=validated_data['creator']
        )
        self.send_verification_email(user)
        return user
    
    def send_verification_email(self, user):
        # Generate verification link using unique_id and get the domain form root directory .env file
        verification_link = f'{settings.DOMAIN_NAME}/verify-email/?unique_id={user.unique_id}'
        
        # Email sending logic (using Django's email functionality)
        subject = 'Verify your email'
        message = f'Please click on the link to verify your email: {verification_link}'
        from_email = 'contact@artixcore.com'  # Replace with your email
        recipient_list = [user.email.strip()]
        send_mail(subject, message, from_email, recipient_list)

        # Increment the email send count
        user.email_verification_send_count += 1
        user.save()

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
    
class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id','menu_name', 'parent_menu', 'sequence', 'menu_link', 'created_at', 'created_by']
        
    def create(self, validated_data):
        menu = Menu.objects.create(
            menu_name=validated_data['menu_name'],
            parent_menu=validated_data['parent_menu'],
            sequence=validated_data['sequence'],
            menu_link=validated_data['menu_link'],
            created_by=validated_data['created_by']
        )
        return menu
    
    def update(self, instance, validated_data):
        instance.menu_name = validated_data.get('menu_name', instance.menu_name)
        instance.parent_menu = validated_data.get('parent_menu', instance.parent_menu)
        instance.sequence = validated_data.get('sequence', instance.sequence)
        instance.menu_link = validated_data.get('menu_link', instance.menu_link)
        instance.save()
        return instance
    
class MenuContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuContent
        fields = ['id','menu_id', 'image', 'title', 'meta_title', 'description', 'created_at']
        
    def create(self, validated_data):
        menu_content = MenuContent.objects.create(
            menu_id=validated_data['menu_id'],
            image=validated_data['image'],
            title=validated_data['title'],
            meta_title=validated_data['meta_title'],
            description=validated_data['description']
        )
        return menu_content
    
    def update(self, instance, validated_data):
        instance.menu_id = validated_data.get('menu_id', instance.menu_id)
        instance.image = validated_data.get('image', instance.image)
        instance.title = validated_data.get('title', instance.title)
        instance.meta_title = validated_data.get('meta_title', instance.meta_title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
    
    
class Contact_formSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact_form
        fields = ['id','name', 'email', 'message', 'created_at']
        
    def create(self, validated_data):
        contact_form = Contact_form.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            message=validated_data['message']
        )
        return contact_form