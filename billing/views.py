from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from users.models import Student, User
from .models import Billing


def bill(request, student_id):
    student = get_object_or_404(Student, user_id=student_id)
    billing = Billing.objects.filter(student=student)
    return render(request, 'bill.html', {'student': student, 'billing': billing})

@login_required
def bill_detail(request, pk):
    bill = get_object_or_404(Billing, pk=pk)
    print(f'bill {bill} - pk {pk} - student {bill.student.user}')
    if bill.student.user != request.user:
        # only display the bill if the associated student matches the currently logged in user
        return render(request, 'error.html', {'message': 'Access Denied'})
    return render(request, 'bill_detail.html', {'student': bill.student, 'bill': bill})
