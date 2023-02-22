from django.contrib import admin
from billing.models import Billing


class BillingAdmin(admin.ModelAdmin):
    list_display = ('typ', 'teacher', 'student', 'description', 'amount', 'is_paid', 'date')
    list_filter = ('typ', 'student', 'teacher', 'is_paid', 'date')

    def get_queryset(self, request):
        qs = super(BillingAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.is_staff:
            return qs.filter(student__class_group=request.user.profile.class_group)
        elif request.user.is_authenticated:
            return qs.filter(student=request.user.profile.student)


admin.site.register(Billing, BillingAdmin)
