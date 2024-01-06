from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, FrontendContent

admin.site.register(CustomUser, UserAdmin)
admin.site.register(FrontendContent)

# Register your models here.
