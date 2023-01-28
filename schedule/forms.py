from django import forms
from datetimewidget.widgets import DateTimeWidget
from .models import Lesson


class LessonModelForm(forms.ModelForm):
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

        widgets = {
            # Use localization and bootstrap 3
            'start_time': DateTimeWidget(attrs={'id': "start_time_id"}, usel10n=True, bootstrap_version=4),
            'end_time': DateTimeWidget(attrs={'id': "end_time_id"}, usel10n=True, bootstrap_version=4)
        }
