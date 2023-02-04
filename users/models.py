from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


# import sys
# import os.path
# Import from sibling directory ..\
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
# from schedule.models import ClassGroup


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone = models.BigIntegerField('phone number', blank=True, null=True)
    address = models.CharField('address', max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.email}'


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment_date = models.DateField()

    def __str__(self):
        return f'{self.user}'


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start_date = models.DateField()

    def __str__(self):
        return f'{self.user}'


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    child = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True, default=None)
    relationship = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.user} - {self.relationship}'


def assign_group(sender, instance, created, **kwargs):
    if created:
        if isinstance(instance, Student):
            group = Group.objects.get(name="Student")
        elif isinstance(instance, Teacher):
            group = Group.objects.get(name="Teacher")
        elif isinstance(instance, Parent):
            group = Group.objects.get(name="Parent")
        else:
            return
        instance.user.groups.add(group)


models.signals.post_save.connect(assign_group, sender=User)
