from django import forms
from datetimewidget.widgets import DateTimeWidget
from django.forms import DateTimeField
from django.forms.widgets import DateInput, DateTimeInput
from .models import Lesson, ClassGroup


class LessonModelForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = [
            'subject',
            'location',
            'start_time',
            'end_time',
            'student',
            'class_group',
            'teacher',
        ]

        widgets = {
            # Use localization and bootstrap 3
            'start_time': DateTimeWidget(attrs={'id': "start_time_id"}, usel10n=True, bootstrap_version=4),
            'end_time': DateTimeWidget(attrs={'id': "end_time_id"}, usel10n=True, bootstrap_version=4)
        }


class TimetableFilterForm(forms.Form):
    class_group = forms.ModelChoiceField(
        queryset=ClassGroup.objects.all(),
        required=False,
        label='Class Group'
    )
    date = forms.DateField(widget=DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'], required=False)


