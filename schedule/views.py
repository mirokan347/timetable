from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from datetime import datetime, timedelta
import calendar
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    ListView,
    DeleteView
)

from logbook.models import Logbook
from .forms import LessonModelForm, TimetableFilterForm
from .models import Lesson, ClassGroup, Location, Subject


class LessonCreateView(UserPassesTestMixin, CreateView):
    model = Lesson
    form_class = LessonModelForm
    template_name = 'lesson/lesson_create.html'
    success_url = reverse_lazy('schedule:lesson-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        lesson = self.object
        class_group = form.cleaned_data.get('class_group')
        students_no_group = form.cleaned_data.get('students')
        subject = form.cleaned_data.get('subject')
        lesson.students.set(students_no_group)
        lesson.save()

        if class_group:
            students = class_group.members.all()
            for student in students:
                Logbook.objects.create(student=student, lesson=lesson, subject=subject)
        if students_no_group:
            for student in students_no_group:
                Logbook.objects.create(student=student, lesson=lesson, subject=subject)

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


@login_required
def timetable_view(request):
    form = TimetableFilterForm(request.GET or None)
    timetable = {}
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    if form.is_valid():
        class_group = form.cleaned_data['class_group']
        date = form.cleaned_data['date']
        date_string = date.strftime('%Y-%m-%d')
        datetime_object = datetime.strptime(date_string, '%Y-%m-%d')
        week = datetime_object.isocalendar()[1]
        # Get lessons for the selected week and class group
        lessons = Lesson.objects.filter(class_group=class_group, start_time__week=week).order_by('start_time__hour',
                                                                                                 'start_time__minute')
        print(lessons)
        for lesson in lessons:
            print(type(lesson))
            day = lesson.start_time.strftime('%A')
            hour = lesson.start_time.strftime('%H:%M')
            if hour not in timetable:
                timetable[hour] = {}
            if day not in timetable[hour]:
                timetable[hour][day] = {}
            timetable[hour][day][lesson.id] = lesson
        print(timetable)
    context = {'form': form,
               'timetable': timetable,
               'days': days
               }
    return render(request, 'timetable/timetable.html', context)
