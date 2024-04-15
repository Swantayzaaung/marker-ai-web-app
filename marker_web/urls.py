from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("practice", views.practice, name="practice"),
    path("results", views.results, name="results")
]