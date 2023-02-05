from django.urls import path
from . import views

app_name = 'logbook'

urlpatterns = [
    path('', views.LogbookListView.as_view(), name='logbook-list'),
    path('<int:id>/', views.LogbookDetailView.as_view(), name='logbook-detail'),
    path('create/', views.LogbookCreateView.as_view(), name='logbook-create'),
    path('logbooks/create/<int:id>/', views.LogbookCreateView.as_view(), name='create_logbooks'),
    path('<int:id>/update/', views.LogbookUpdateView.as_view(), name='logbook-update'),
    path('<int:id>/delete/', views.LogbookDeleteView.as_view(), name='logbook-delete'),
]
