from django import forms
from django.forms import modelformset_factory

from .models import Logbook


class LogbookForm(forms.ModelForm):

    class Meta:
        model = Logbook
        fields = ['student', 'lesson', 'subject', 'attendance', 'grade', 'comment']


class LogbookUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LogbookUpdateForm, self).__init__(*args, **kwargs)
        self.fields['student'].disabled = True
        self.fields['lesson'].disabled = True
        self.fields['subject'].disabled = True

    class Meta:
        model = Logbook
        fields = ['student', 'lesson', 'subject', 'attendance', 'grade', 'comment']


class LogbookFormSet(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LogbookFormSet, self).__init__(*args, **kwargs)
        self.fields['student'].disabled = True

    class Meta:
        model = Logbook
        fields = ['student', 'attendance', 'grade']
