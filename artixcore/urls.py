from django.urls import re_path,include
from django.contrib import admin
urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path('' , include('admin_app.urls')),
]
