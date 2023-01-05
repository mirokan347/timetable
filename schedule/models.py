from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import Group
import sys
import os.path
# Import from sibling directory ..\
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from users.models import CustomUser


class Subject(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Location(models.Model):
    name = models.CharField(max_length=50)
    nr_seats = models.IntegerField()

    def __str__(self):
        return self.name

class ClassGroup(models.Model):
    name = models.CharField(max_length=50)
    members = models.ManyToManyField(CustomUser, through='ClassGroupMembership')
    year = models.CharField(max_length=50, default=None)

    def __str__(self):
        return self.name


class ClassGroupMembership(models.Model):
    pupil = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.pupil} - {self.group}'


class Lesson(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    '''pupil = models.ForeignKey(CustomUser, related_name='pupil', on_delete=models.CASCADE,
                              default=None)'''
    teacher = models.ForeignKey(CustomUser, related_name='teacher', on_delete=models.CASCADE,
                                default=None)
    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE, default=None)

    def get_absolute_url(self):
        return reverse("schedule:lesson-detail", kwargs={"id": self.id})

    def __str__(self):
        return f'{self.subject} - {self.class_group} - {self.location}'

