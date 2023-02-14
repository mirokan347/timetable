from django import forms

from .models import Student


class BillFilterForm(forms.Form):
    student = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        parent = kwargs.pop('parent', None)
        super().__init__(*args, **kwargs)
        if parent:
            self.fields['student'].queryset = parent.students.all()
