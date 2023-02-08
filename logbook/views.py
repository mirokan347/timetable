from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from schedule.models import Lesson
from .forms import LogbookForm, LogbookFormSet, LogbookUpdateForm
from .models import Logbook


class LogbookListView(UserPassesTestMixin, ListView):
    model = Logbook
    template_name = 'logbook_list.html'
    context_object_name = 'logbooks'

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
        return redirect('error.html', {'message': 'Access Denied'})

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


def logbook_update(request, lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    curr_grades = Logbook.objects.filter(lesson=lesson)
    if not request.user.groups.filter(name='teacher').exists():
        print(request.user.groups.filter(name='teacher'))
        return render(request, 'error.html', {'message': 'Access Denied'})

    queryset = Logbook.objects.filter(lesson=lesson)

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

