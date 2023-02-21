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
from .forms import LessonModelForm, TimetableFilterForm, TimetableTeacherFilterForm
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
    context_object_name = 'lessons'
    model = Lesson

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = TimetableTeacherFilterForm(self.request.GET or None)
        context['form'] = form

        return context

    def get_queryset(self):
        queryset = super().get_queryset().order_by('start_time')
        class_group_id = self.request.GET.get('class_group', None)
        date = self.request.GET.get('date', None)
        teacher_id = self.request.GET.get('teacher', None)
        if class_group_id:
            queryset = queryset.filter(class_group_id=class_group_id)
        if date:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            start_date = date_obj - timedelta(days=date_obj.weekday())
            end_date = start_date + timedelta(days=6)
            queryset = queryset.filter(start_time__range=(start_date, end_date)).order_by('start_time')
        if teacher_id:
            queryset = queryset.filter(teacher__id=teacher_id)
        return queryset


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
    def week_days(date_):
        lst = []
        days_ = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        start_of_week = date_ - timedelta(days=date_.weekday())
        for i, week_day in enumerate(days_):
            date_day = start_of_week + timedelta(days=i)
            lst.append(f"{week_day}\n{date_day.strftime('%d.%m.%Y')}")
        return lst

    days = name_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    form = TimetableFilterForm(request.user, data=request.GET)
    timetable = {}

    if form.is_valid():
        class_group = form.cleaned_data['class_group']
        student = form.cleaned_data['student']
        date = form.cleaned_data['date']
        if date:
            date_string = date.strftime('%Y-%m-%d')
            datetime_object = datetime.strptime(date_string, '%Y-%m-%d')
            week = datetime_object.isocalendar()[1]
            # Get lessons for the selected week and class group
            if class_group:
                lessons = Lesson.objects.filter(class_group=class_group, start_time__week=week).order_by(
                    'start_time__hour', 'start_time__minute')
            elif student:
                lessons = Lesson.objects.filter(students__id=student.id, start_time__week=week).order_by(
                    'start_time__hour', 'start_time__minute')
            else:
                lessons = Lesson.objects.filter(start_time__week=week).order_by('start_time__hour', 'start_time__minute')
            name_days = week_days(date)
            for lesson in lessons:
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
               'days': days,
               'name_days': name_days
               }
    return render(request, 'timetable/timetable.html', context)
