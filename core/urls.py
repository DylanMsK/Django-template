from django.urls import path
from core import views

app_name = "system"

urlpatterns = [
    path("health/", views.HealthCheck.as_view(), name="health"),
    path("info/", views.ProjectInfo.as_view(), name="info"),
]
