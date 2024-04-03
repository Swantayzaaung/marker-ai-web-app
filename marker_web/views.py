from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    available_years
    return render(request, "marker_web/index.html")

def about(request):
    return render(request, "marker_web/about.html")

def practice(request):
    return render(request, "marker_web/practice.html")

def results(request):
    return render(request, "marker_web/results.html")