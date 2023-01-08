from django.urls import path
from users.views import (
    register_view,

)

app_name = 'users'

urlpatterns = [
    path('register/', register_view, name="register"),
]