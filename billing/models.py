from django.db import models

from users.models import Student, Teacher


class Billing(models.Model):
    date = models.DateField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    PAYMENT = 'Payment'
    BILL = 'Bill'
    TYP_CHOICES = [
        (PAYMENT, 'Payment'),
        (BILL, 'Bill'),
    ]
    typ = models.CharField(choices=TYP_CHOICES, max_length=10)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.student} - {self.description}'
