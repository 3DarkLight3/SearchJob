from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=40, verbose_name='First name')
    last_name = models.CharField(max_length=60, verbose_name='Last name')
