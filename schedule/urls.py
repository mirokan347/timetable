from django.urls import path
from .views import (LessonListView,
                    LessonCreateView,
                    LessonDetailView,
                    LessonUpdateView,
                    LessonDeleteView
                    )

app_name = 'schedule'

urlpatterns = [
    path('', LessonListView.as_view(), name='lesson-list'),
    path('create/', LessonCreateView.as_view(), name='lesson-create'),
    path('<int:id>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('<int:id>/update/', LessonUpdateView.as_view(), name='lesson-update'),
    path('<int:id>/delete/', LessonDeleteView.as_view(), name='lesson-delete'),
]