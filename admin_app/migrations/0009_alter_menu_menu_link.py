# Generated by Django 5.0.1 on 2024-02-13 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0008_alter_menucontent_menu_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='menu_link',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
