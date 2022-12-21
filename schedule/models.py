from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import Group


class Subject(models.Model):
    title = models.CharField(max_length=50)


class Location(models.Model):
    name = models.CharField(max_length=50)
    nr_seats = models.IntegerField()


'''class PupilsClass(models.Model):
    name = models.CharField(max_length=50)'''


class Lesson(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    pupil = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    # Spupils_class = models.ForeignKey(PupilsClass, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("lesson:lesson-detail", kwargs={"id": self.id})
