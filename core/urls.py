from django.urls import path
from core import views

urlpatterns = [
    path("health/", views.ProjectInfo.as_view()),
    path("info/", views.ProjectInfo.as_view()),
]
