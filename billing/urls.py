from django.urls import path
from .views import bill, bill_detail, payment, payment_detail, bill_view

app_name = 'billing'

urlpatterns = [
    path('<int:user_id>/bill/', bill, name='bill'),
    path('bill/<int:pk>/', bill_detail, name='bill-detail'),
    path('<int:user_id>/payment/', payment, name='payment'),
    path('payment/<int:pk>/', payment_detail, name='payment-detail'),
    path('<int:user_id>/bills/', bill_view, name='bill_view'),
]
