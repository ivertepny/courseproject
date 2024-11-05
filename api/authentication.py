from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("X-Custom-Token")
        if not token or token != "mysecrettoken":
            raise AuthenticationFailed("Invalid or missing token")
        try:
            user = User.objects.get(username="my_user")
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed("No such user")
