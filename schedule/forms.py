from django import forms

from .models import Lesson


class LessonModelForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = [
            'start_time',
            'end_time',
            'pupil',
            'class_group',
        ]
