# Generated by Django 5.0.1 on 2024-01-05 19:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0002_alter_customuser_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='FrontendContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_type', models.CharField(choices=[('hero_section', 'Hero Section'), ('about_section', 'About Section'), ('services_section', 'Services Section'), ('blog_section', 'Blog Section'), ('projects_section', 'Projects Section'), ('protfolio_section', 'Protfolio Section'), ('reviews_section', 'Reviews Section'), ('pricing_section', 'Pricing Section'), ('team_section', 'Team Section'), ('contact_section', 'Contact Section'), ('social_links', 'Social Links'), ('footer_section', 'Footer Section')], max_length=20, unique=True)),
                ('title_type', models.CharField(choices=[('main_content', 'Main Content'), ('sub_content', 'Sub Content')], max_length=20, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='frontend_content_images/')),
                ('content', models.JSONField(blank=True, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
