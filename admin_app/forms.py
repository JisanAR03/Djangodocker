from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPES, required=False)
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'user_type')
        
    def save(self, commit=True):
        user = super().save(commit=False)
        # if user is not logged in and user_type is not provided then it will be general_user
        if not user.is_authenticated and not self.cleaned_data.get('user_type'):
            user.user_type = 'general_user'
        if commit:
            user.save()
        return user