from django.contrib import admin

from .models import (Lesson,
                     ClassGroup,
                     ClassGroupMembership,
                     Location,
                     Subject
                     )

admin.site.register(Lesson)
admin.site.register(ClassGroup)
admin.site.register(ClassGroupMembership)
admin.site.register(Location)
admin.site.register(Subject)
