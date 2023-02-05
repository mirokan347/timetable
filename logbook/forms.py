from django import forms
from django.forms import formset_factory

from .models import Logbook


class LogbookForm(forms.ModelForm):

    class Meta:
        model = Logbook
        fields = ['student', 'lesson', 'subject', 'attendance', 'grade', 'comment']

