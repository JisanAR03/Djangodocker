from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, FrontendContent, Menu, MenuContent

admin.site.register(CustomUser, UserAdmin)
admin.site.register(FrontendContent)
admin.site.register(Menu)
admin.site.register(MenuContent)

# Register your models here.
