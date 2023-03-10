from django.urls import path
from . import views
from .views import logbook_parent_view

app_name = 'logbook'

urlpatterns = [
    path('list/', views.LogbookListView.as_view(), name='logbook-list'),
    path('<int:id>/', views.LogbookDetailView.as_view(), name='logbook-detail'),
    path('create/', views.LogbookCreateView.as_view(), name='logbook-create'),
    path('<int:id>/update/', views.LogbookUpdateView.as_view(), name='logbook-update'),
    path('<int:lesson_id>/updates/', views.logbook_update, name='logbook_update'),
    path('<int:id>/delete/', views.LogbookDeleteView.as_view(), name='logbook-delete'),
    path('<int:user_id>/list/', logbook_parent_view, name='logbook_parent_view'),
]
