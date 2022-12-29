from django import forms

from .models import Lesson


class LessonModelForm(forms.ModelForm):
    start_time = forms.DateTimeField()
    end_time = forms.DateTimeField()

    class Meta:
        model = Lesson
        fields = [
            'subject',
            'location',
            'start_time',
            'end_time',
            'pupil',
            'class_group',
            'teacher',
        ]
