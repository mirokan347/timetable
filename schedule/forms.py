from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Button
from django import forms
from datetimewidget.widgets import DateTimeWidget
from django.forms import DateTimeField
from django.forms.widgets import DateInput, DateTimeInput

from users.models import Student, Teacher, Parent
from .models import Lesson, ClassGroup


class LessonModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'subject',
                'location',
                'start_time',
                'end_time',
                'students',
                'class_group',
                'teacher',
            ),
            ButtonHolder(
                Submit('submit', 'Save', css_class='btn-success'),
                Button('cancel', 'Cancel', onclick='window.history.go(-1);', css_class='btn-default')
            )
        )
        self.fields['students'].widget.attrs.update({'size': 10, 'class': 'form-control overflow-auto'})

    class Meta:
        model = Lesson
        fields = [
            'subject',
            'location',
            'start_time',
            'end_time',
            'students',
            'class_group',
            'teacher',
        ]

        widgets = {
            # Use localization and bootstrap 4
            'start_time': DateTimeWidget(attrs={'id': "start_time_id"}, usel10n=True, bootstrap_version=4),
            'end_time': DateTimeWidget(attrs={'id': "end_time_id"}, usel10n=True, bootstrap_version=4),
        }

    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    def clean_students(self):
        students = self.cleaned_data.get('students')
        if not students:
            return []

        return list(Student.objects.filter(id__in=students))

    '''def save(self, commit=True):
        instance = super().save(commit=False)

        students = self.cleaned_data.get('students', [])
        instance.students.set(students)

        if commit:
            instance.save()

        return instance'''


class TimetableFilterForm(forms.Form):
    class_group = forms.ModelChoiceField(
        queryset=ClassGroup.objects.all(),
        required=False,
        empty_label='All',
        label='Class Group'
    )
    date = forms.DateField(
        widget=DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'], required=False
    )

    def __init__(self, user, *args, **kwargs):
        super(TimetableFilterForm, self).__init__(*args, **kwargs)
        if user.groups.filter(name='teacher').exists():
            self.fields['student'] = forms.ModelChoiceField(queryset=Student.objects.all(), required=False)
        elif user.groups.filter(name='student').exists():
            self.fields['student'] = forms.ModelChoiceField(queryset=Student.objects.filter(user=user), required=False)
        elif user.groups.filter(name='parent').exists():
            parent = Parent.objects.get(user=user)
            students = parent.students.values_list('id', flat=True)
            self.fields['student'] = forms.ModelChoiceField(queryset=Student.objects.filter(id__in=students), required=False)


class TimetableTeacherFilterForm(forms.Form):
    class_group = forms.ModelChoiceField(
        queryset=ClassGroup.objects.all(),
        required=False,
        empty_label='All',
        label='Class Group'
    )
    date = forms.DateField(
        widget=DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'], required=False
    )
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all(), required=False)
