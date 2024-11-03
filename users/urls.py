# Мій файл urls

from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView, PasswordChangeDoneView
# from django.views.generic import TemplateView

from users.views import (
    UserLoginView,
    UserRegistrationView,
    UserProfileView,
    EmailVerificationView,
    UserPasswordChange,
    VerificationFailureView,
    # UserPasswordReset,
    # UserPasswordResetConfirm,
)

app_name = 'users'  # Namespace for URL names

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification'),
    path('password-change/', UserPasswordChange.as_view(), name="password_change"),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"),
         name="password_change_done"),
    path('verification-failure/', VerificationFailureView.as_view(), name='verification_failure'),
    # path('password-reset/', UserPasswordReset.as_view(), name="password_reset"),
    # # path('password_reset/done/', TemplateView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', UserPasswordResetConfirm.as_view(), name='password_reset_confirm'),
    # path('reset/done/', TemplateView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]
