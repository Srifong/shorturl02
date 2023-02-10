from app.views import UserCreate
from django.urls import path

app_name='api'

urlpatterns = [
path("users/",UserCreate.as_view(), name="user_create"),
]