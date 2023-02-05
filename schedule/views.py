from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    ListView,
    DeleteView
)

from logbook.models import Logbook
from .forms import LessonModelForm
from .models import Lesson


class LessonCreateView(UserPassesTestMixin, CreateView):
    model = Lesson
    form_class = LessonModelForm
    template_name = 'lesson/lesson_create.html'
    success_url = reverse_lazy('schedule:lesson-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        class_group = form.cleaned_data.get('class_group')
        student1 = form.cleaned_data.get('student')
        subject = form.cleaned_data.get('subject')
        if class_group:
            students = class_group.members.all()
            for student in students:
                Logbook.objects.create(student=student, lesson=self.object, subject=subject)
        if student1:
            Logbook.objects.create(student=student, lesson=self.object, subject=subject)
        return response

    def test_func(self):
        return self.request.user.has_perm('schedule.create_lesson')

    def handle_no_permission(self):
        return redirect('/no_permission/')


class LessonListView(ListView):
    template_name = 'lesson/lesson_list.html'
    queryset = Lesson.objects.all()


class LessonDetailView(DetailView):
    template_name = 'lesson/lesson_detail.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Lesson, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class LessonUpdateView(UpdateView):
    template_name = 'lesson/lesson_create.html'
    form_class = LessonModelForm

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Lesson, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class LessonDeleteView(DeleteView):
    template_name = 'lesson/lesson_delete.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Lesson, id=id_)

    def get_success_url(self):
        return reverse('schedule:lesson-list')









