from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    pass
    # image = models.ImageField(upload_to='users_images', null=True, blank=True)
    # date_of_birth = models.DateField(null=True, blank=True)
