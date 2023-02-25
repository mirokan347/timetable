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
    phone = models.CharField(blank=True, null=True, max_length=16, help_text='Contact phone number')
    address = models.TextField('address', max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.id})'


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment_date = models.DateField()

    def save(self, *args, **kwargs):
        student_group, created = Group.objects.get_or_create(name='student')
        self.user.groups.add(student_group)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user}'


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start_date = models.DateField()

    def save(self, *args, **kwargs):
        teacher_group, created = Group.objects.get_or_create(name='teacher')
        self.user.groups.add(teacher_group)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user}'


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name='parents')
    relationship = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        parent_group, created = Group.objects.get_or_create(name='parent')
        self.user.groups.add(parent_group)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} - {self.relationship}'

