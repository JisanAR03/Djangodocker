# Generated by Django 5.0.1 on 2024-01-07 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0004_alter_customuser_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='frontendcontent',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
