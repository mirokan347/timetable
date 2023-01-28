from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    ListView,
    DeleteView
)

from .forms import LessonModelForm
from .models import Lesson


class LessonCreateView(CreateView):
    template_name = 'lesson/lesson_create.html'
    form_class = LessonModelForm
    queryset = Lesson.objects.all()

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


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









