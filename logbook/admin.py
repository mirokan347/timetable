from django.contrib import admin
from .models import Logbook


class LogBookAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'subject', 'student', 'attendance', 'grade', 'comment')
    list_filter = ('student', 'lesson__class_group', 'lesson__subject')

    def get_queryset(self, request):
        qs = super(LogBookAdmin, self).get_queryset(request)
        if request.user.is_superuser or request.user.is_staff:
            return qs


admin.site.register(Logbook, LogBookAdmin)
