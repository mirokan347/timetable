from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import authenticate, get_user_model

from .models import User, Teacher, Student, Parent


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'address')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'address')


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % user)


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")


class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'address')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = User.objects.exclude(pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def save(self, commit=True):
        account = super(AccountUpdateForm, self).save(commit=False)
        account.email = self.cleaned_data['email'].lower()
        account.first_name = self.cleaned_data['first_name']
        account.last_name = self.cleaned_data['last_name']
        if commit:
            account.save()
        return account


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = get_user_model().objects.filter(groups__isnull=True)


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = get_user_model().objects.filter(groups__isnull=True)


class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = get_user_model().objects.filter(groups__isnull=True)
