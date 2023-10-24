from django.urls import path
from core import views

urlpatterns = [
    path("get/", views.sample_get),
    path("post/", views.sample_post),
    path("error/", views.sample_error),
]
