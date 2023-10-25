from django.urls import path
from core import views

urlpatterns = [
    path("get/", views.SampleGetViewset.as_view()),
    path("post/", views.SamplePostViewset.as_view()),
    path("error/", views.sample_error),
]
