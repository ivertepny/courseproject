import uuid
from datetime import timedelta

from celery import shared_task

from django.utils.timezone import now
from users.models import User, EmailVerification #, PasswordReset


@shared_task
# @shared_task(bind=True, time_limit=300)  # 5 minutes timeout
def send_email_verification(user_id):
    print("Hello")
    user = User.objects.get(id=user_id)
    expiration = now() + timedelta(minutes=10)
    record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
    record.send_verification_email()


# @shared_task
# def send_password_reset_email(user_id):
#     user = User.objects.get(id=user_id)
#     expiration = now() + timedelta(minutes=10)
#     record = PasswordReset.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
#     record.send_reset_password_email()
