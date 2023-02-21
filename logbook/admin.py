from django.contrib import admin
from .models import Logbook


class LogBookAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'subject', 'student', 'attendance', 'grade', 'comment')
    list_filter = ('student', 'lesson__class_group', 'lesson__subject')

    def get_queryset(self, request):
        qs = super(LogBookAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.is_staff:
            return qs.filter(student__class_group=request.user.profile.class_group)
        elif request.user.is_authenticated:
            return qs.filter(student=request.user.profile.student)


admin.site.register(Logbook, LogBookAdmin)
