from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from users.models import Student, User, Teacher, Parent
from .form import BillFilterForm
from .models import Billing


@login_required
def bill(request, user_id):
    student = get_object_or_404(Student, user_id=user_id)
    billing = Billing.objects.filter(student=student)
    return render(request, 'bill.html', {'student': student, 'billing': billing})


@login_required
def bill_detail(request, pk):
    bill = get_object_or_404(Billing, pk=pk)
    print(f'bill {bill} - pk {pk} - student {bill.student.user}')
    logged_parent = None
    if request.user.groups.filter(name='parent').exists():
        logged_parent = get_object_or_404(Parent, user_id=request.user)
    parent_list = Parent.objects.filter(students=bill.student)
    print(f'{parent_list} - {logged_parent}')
    if bill.student.user == request.user or logged_parent in parent_list:
        return render(request, 'bill_detail.html', {'student': bill.student, 'bill': bill})
    else:
        return render(request, 'error.html', {'message': 'Access Denied'})


@login_required
def payment(request, user_id):
    teacher = get_object_or_404(Teacher, user_id=user_id)
    pay = Billing.objects.filter(teacher=teacher)
    return render(request, 'payment.html', {'teacher': teacher, 'payment': pay})


@login_required
def payment_detail(request, pk):
    pay = get_object_or_404(Billing, pk=pk)
    print(f'bill {pay} - pk {pk} - teacher {pay.teacher.user}')
    if pay.teacher.user != request.user:
        return render(request, 'error.html', {'message': 'Access Denied'})
    return render(request, 'payment_detail.html', {'teacher': pay.teacher, 'pay': pay})


@login_required
def bill_view(request, user_id):
    if request.user.groups.filter(name='parent').exists():
        parent = get_object_or_404(Parent, user_id=user_id)
        form = BillFilterForm(request.POST or None, parent=parent)
        if form.is_valid():
            student = form.cleaned_data.get('student')
            billing = Billing.objects.filter(student=student)
            context = {
                'form': form,
                'student': student,
                'billing': billing
            }
            return render(request, 'bill_parent.html', context)
    else:
        form = None
    context = {'form': form}
    return render(request, 'bill_parent.html', context)

