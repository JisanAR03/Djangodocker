# Generated by Django 5.0.1 on 2024-03-11 10:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0012_contact_form_menucontent_icon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menucontent',
            name='menu_id',
        ),
        migrations.AddField(
            model_name='menucontent',
            name='menu',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_app.menu'),
        ),
    ]
