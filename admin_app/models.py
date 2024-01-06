from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_TYPES = [
        ('supreme_admin', 'Supreme Admin'),
        ('admin', 'Admin'),
        ('content_writer', 'Content Writer'),
        ('ad_manager', 'Ad Manager'),
        ('accountant', 'Accountant'),
        ('hr', 'HR'),
        ('developer', 'Developer'),
        ('data_scientist', 'Data Scientist'),
        ('blogger', 'Blogger'),
        ('designer', 'Designer'),
        ('general_user', 'General User'),
    ]
    user_type = models.CharField(max_length=15, choices=USER_TYPES, default='general_user')
    email = models.EmailField(unique=True)
    
class FrontendContent(models.Model):
    CONTENT_TYPES = [
        ('hero_section', 'Hero Section'),
        ('about_section', 'About Section'),
        ('services_section', 'Services Section'),
        ('blog_section', 'Blog Section'),
        ('projects_section', 'Projects Section'),
        ('protfolio_section', 'Protfolio Section'),
        ('reviews_section', 'Reviews Section'),
        ('pricing_section', 'Pricing Section'),
        ('team_section', 'Team Section'),
        ('contact_section', 'Contact Section'),
        ('social_links', 'Social Links'),
        ('footer_section', 'Footer Section'),
    ]
    TITLE_TYPES = [
        ('main_content', 'Main Content'),
        ('sub_content', 'Sub Content'),
    ]
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    title_type = models.CharField(max_length=20, choices=TITLE_TYPES)
    image = models.ImageField(upload_to='frontend_content_images/',blank=True,null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True,null=True)
    content = models.JSONField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content_type