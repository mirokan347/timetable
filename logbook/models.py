from django.db import models

# Create your models here.
from django.urls import reverse

from schedule.models import Subject, Lesson
from users.models import Student, Teacher


class Logbook(models.Model):
    student = models.OneToOneField(Student, related_name='logbook', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='logbook', on_delete=models.CASCADE, default=None)
    lesson = models.ForeignKey(Lesson, related_name='logbook', on_delete=models.CASCADE, default=None)
    grade = models.CharField(max_length=20, default=None, blank=True, null=True)
    comment = models.TextField(default=None, blank=True, null=True)
    PRESENT = "P"
    ABSENT = "A"
    EXCUSED = "E"
    STATUS_CHOICES = [
        (PRESENT, "Present"),
        (ABSENT, "Absent"),
        (EXCUSED, "Excused"),
    ]
    attendance = models.CharField(max_length=1, choices=STATUS_CHOICES, default=None, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("logbook:logbook-detail", kwargs={"id": self.id})

    def __str__(self):
        return f"{self.student} - {self.attendance} - {self.grade}"
