from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
# import sys
# import os.path
# Import from sibling directory ..\
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
# from schedule.models import ClassGroup


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
