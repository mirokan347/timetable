from django.urls import path
from .views import bill, bill_detail

app_name = 'billing'

urlpatterns = [
    path('<int:student_id>/bill/', bill, name='bill'),
    path('bill/<int:pk>/', bill_detail, name='bill-detail'),
]
