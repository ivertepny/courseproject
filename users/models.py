from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils.timezone import now


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)
    is_no_social_user = models.BooleanField(default=False)  # Default for regular email/password users


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f"Email Verification object for: {self.user.email}"

    def send_verification_email(self):
        link = reverse("users:email_verification", kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f' {settings.DOMAIN_NAME}{link}'
        subject = f'Підтвердження для облікового запису для {self.user.username}'
        message = 'Для підтвердження обліковго запису для {} перейдіть за посиланням {}'.format(
            self.user.email,
            verification_link)
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() >= self.expiration else False


# class PasswordReset(models.Model):
#     code = models.UUIDField(unique=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     expiration = models.DateTimeField()
#
#     def __str__(self):
#         return f"Password Reset object for: {self.user.email}"
#
#     def send_reset_password_email(self):
#         link = reverse("users:password_reset_confirm", kwargs={'uidb64': self.user.id, 'token': self.code})
#         reset_link = f' {settings.DOMAIN_NAME}{link}'
#         subject = f'Скидання пароля для {self.user.username}'
#         message = 'Для скидання пароля для {} перейдіть за посиланням {}'.format(
#             self.user.email,
#             reset_link)
#         send_mail(
#             subject=subject,
#             message=message,
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[self.user.email],
#             fail_silently=False,
#         )
#
#     def is_expired(self):
#         return True if now() >= self.expiration else False
#
