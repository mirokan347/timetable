from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import Group
import sys
import os.path
# Import from sibling directory ..\
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from users.models import User, Teacher, Student


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
    members = models.ManyToManyField(Student, through='ClassGroupMembership')
    year = models.CharField(max_length=50, default=None)

    def __str__(self):
        return f'{self.name} - {self.year}'


class ClassGroupMembership(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.student} - {self.group}'


class Lesson(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    students = models.ManyToManyField(Student, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, default=None)
    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE, blank=True, null=True, default=None)

    def get_absolute_url(self):
        return reverse("schedule:lesson-detail", kwargs={"id": self.id})

    def __str__(self):
        return f'{self.subject} \n {self.class_group} \n {self.location}'

