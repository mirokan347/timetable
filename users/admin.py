from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm, TeacherForm, ParentForm, StudentForm
from .models import User, Teacher, Student, Parent


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active',)
    list_filter = ('email', 'first_name', 'last_name', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'groups')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'groups', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('email', 'first_name', 'last_name',)


class TeacherAdmin(admin.ModelAdmin):
    form = TeacherForm
    list_display = ('first_name', 'last_name', 'email', 'start_date', 'is_staff', 'is_active')

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def email(self, obj):
        return obj.user.email

    def is_staff(self, obj):
        return obj.user.is_staff

    def is_active(self, obj):
        return obj.user.is_active


class StudentAdmin(admin.ModelAdmin):
    form = StudentForm
    list_display = ('first_name', 'last_name', 'email', 'enrollment_date', 'is_staff', 'is_active')

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def email(self, obj):
        return obj.user.email

    def is_staff(self, obj):
        return obj.user.is_staff

    def is_active(self, obj):
        return obj.user.is_active


class ParentAdmin(admin.ModelAdmin):
    form = ParentForm
    list_display = ('first_name', 'last_name', 'email', 'is_staff', 'is_active')

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def email(self, obj):
        return obj.user.email

    def is_staff(self, obj):
        return obj.user.is_staff

    def is_active(self, obj):
        return obj.user.is_active


admin.site.register(User, CustomUserAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Parent, ParentAdmin)
