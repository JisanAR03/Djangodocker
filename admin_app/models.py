from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class CustomUser(AbstractUser):
    USER_TYPES = [
        ('supreme_admin', 'Supreme Admin'),
        ('admin', 'Admin'),
        ('content_writer_admin', 'Content Writer Admin'),
        ('content_writer', 'Content Writer'),
        ('ad_manager_admin', 'Ad Manager Admin'),
        ('ad_manager', 'Ad Manager'),
        ('accountant_admin', 'Accountant Admin'),
        ('accountant', 'Accountant'),
        ('hr_admin', 'HR Admin'),
        ('hr', 'HR'),
        ('developer_admin', 'Developer Admin'),
        ('developer', 'Developer'),
        ('data_scientist_admin', 'Data Scientist Admin'),
        ('data_scientist', 'Data Scientist'),
        ('blogger_admin', 'Blogger Admin'),
        ('blogger', 'Blogger'),
        ('designer_admin', 'Designer Admin'),
        ('designer', 'Designer'),
        ('general_user', 'General User'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='general_user')
    email = models.EmailField(unique=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_verified = models.BooleanField(default=False)
    email_verification_send_count = models.IntegerField(default=0)
    creator = models.ForeignKey('self', on_delete=models.CASCADE,blank=True,null=True)
    
class FrontendContent(models.Model):
    content_type = models.CharField(max_length=50)
    image = models.ImageField(upload_to='frontend_content_images/',blank=True,null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True,null=True)
    content = models.JSONField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.content_type
    
class Menu(models.Model):
    menu_name = models.CharField(max_length=100)
    parent_menu = models.ForeignKey('self', on_delete=models.CASCADE,blank=True,null=True)
    sequence = models.IntegerField(blank=True,null=True)
    menu_link = models.CharField(max_length=100,unique=True,blank=True,null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.menu_name
    
class MenuContent(models.Model):
    menu = models.OneToOneField(Menu, on_delete=models.CASCADE, related_name='menucontent',blank=True,null=True)
    image = models.ImageField(upload_to='menu_content_images/',blank=True,null=True)
    icon = models.ImageField(upload_to='menu_content_icons/',blank=True,null=True)
    title = models.CharField(max_length=100)
    meta_title = models.CharField(max_length=100,blank=True,null=True)
    description = models.JSONField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
class Contact_form(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name