from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

userModel = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = userModel.objects.get(email=email)
        except userModel.DoesNotExist:
            return None
        if user is not None and user.check_password(password):
            if user.is_verified:
                return user
        return None