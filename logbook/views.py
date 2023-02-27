from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from schedule.models import Lesson
from users.models import Parent
from .forms import LogbookForm, LogbookFormSet, LogbookUpdateForm, LogbookFilterForm
from .models import Logbook


class LogbookListView(UserPassesTestMixin, ListView):
    model = Logbook
    template_name = 'logbook_list.html'
    context_object_name = 'logbooks'

    def get_queryset(self):
        queryset = super().get_queryset()
        lesson_id = self.request.GET.get('lesson')
        user_id = self.request.GET.get('student')
        print(user_id)
        print(self.request.user.id)
        if lesson_id and self.request.user.groups.filter(name='teacher').exists():
            return Logbook.objects.filter(lesson_id=lesson_id)
        elif int(user_id) == int(self.request.user.id):
            return Logbook.objects.filter(student__user_id=user_id)
        else:
            print('no permission')

    def test_func(self):
        return self.request.user.has_perm('logbook.view_logbook')

    def handle_no_permission(self):
        return redirect('/no_permission/')


class LogbookDetailView(UserPassesTestMixin, DetailView):
    model = Logbook
    template_name = 'logbook_detail.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Logbook, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def test_func(self):
        return self.request.user.has_perm('logbook.view_logbook')

    def handle_no_permission(self):
        return redirect('/no_permission/')


class LogbookCreateView(UserPassesTestMixin, CreateView):
    model = Logbook
    form_class = LogbookForm
    template_name = 'logbook_form.html'
    success_url = reverse_lazy('logbook:logbook-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def test_func(self):
        user = self.request.user
        if user.is_authenticated and user.groups.filter(name='teacher').exists():
            # Allow teachers who are also is_staff users to create lessons
            if user.is_staff:
                return True
            else:
                # Deny permission for non-is_staff teachers
                return False
        else:
            return self.request.user.has_perm('logbook.create_logbook')

    def handle_no_permission(self):
        return redirect('/no_permission/')


class LogbookUpdateView(UserPassesTestMixin, UpdateView):
    model = Logbook
    form_class = LogbookUpdateForm
    template_name = 'logbook_form.html'

    def test_func(self):
        return self.request.user.has_perm('logbook.delete_logbook')

    def handle_no_permission(self):
        return redirect('/no_permission/')

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Logbook, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class LogbookDeleteView(UserPassesTestMixin, DeleteView):
    model = Logbook
    template_name = 'logbook_confirm_delete.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Logbook, id=id_)

    def get_success_url(self):
        return reverse('schedule:lesson-list')

    def test_func(self):
        return self.request.user.has_perm('logbook.delete_logbook')

    def handle_no_permission(self):
        return redirect('/no_permission/')


@login_required
def logbook_update(request, lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    curr_grades = Logbook.objects.filter(lesson=lesson)
    if not request.user.groups.filter(name='teacher').exists():
        print(request.user.groups.filter(name='teacher'))
        return render(request, 'error.html', {'message': 'Access Denied'})

    queryset = Logbook.objects.filter(lesson=lesson).order_by('student_id')

    logbookFormSet = modelformset_factory(Logbook, form=LogbookFormSet, extra=0)

    if request.method == 'POST':
        formset = logbookFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.save()
            return redirect('schedule:lesson-detail', id=lesson_id)
        else:
            print(formset.errors)
    else:
        formset = logbookFormSet(queryset=queryset)

    return render(
        request, 'logbook_update_form.html', {'formset': formset, 'form': lesson},
    )


@login_required
def logbook_parent_view(request, user_id):
    if request.user.groups.filter(name='parent').exists():
        parent = get_object_or_404(Parent, user_id=user_id)
        form = LogbookFilterForm(request.POST or None, parent=parent)
        if form.is_valid():
            student = form.cleaned_data.get('student')
            logbooks = Logbook.objects.filter(student=student).order_by('lesson__start_time')
            context = {
                'form': form,
                'student': student,
                'logbooks': logbooks
            }
            return render(request, 'logbook_parent.html', context)
    else:
        form = None
    context = {'form': form}
    return render(request, 'logbook_parent.html', context)