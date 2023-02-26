from django.contrib import admin
from billing.models import Billing


class BillingAdmin(admin.ModelAdmin):
    list_display = ('typ', 'teacher', 'student', 'description', 'amount', 'is_paid', 'date')
    list_filter = ('typ', 'student', 'teacher', 'is_paid', 'date')

    def get_queryset(self, request):
        qs = super(BillingAdmin, self).get_queryset(request)
        if request.user.is_superuser or request.user.is_staff:
            return qs


admin.site.register(Billing, BillingAdmin)
