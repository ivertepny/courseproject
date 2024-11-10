from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class EmailOrUsernameAuthBackend(BaseBackend):
    def clean_email(self, email):
        if not email:
            raise ValidationError('Email is required')
        return email
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to fetch the user by username or email
            user = User.objects.get(email=username) if '@' in username else User.objects.get(username=username)

            # перевіряємо password
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
