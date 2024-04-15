from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from .helpers import extractQP

import requests, tempfile, os

# Create your views here.

def index(request):
    print("hello wrold")
    return render(request, "marker_web/index.html")

def about(request):
    print("about page")
    return render(request, "marker_web/about.html")

def practice(request):
    # https://stackoverflow.com/questions/34503412/download-and-save-pdf-file-with-python-requests-module
    filename = f"{request.GET['subject']}_{request.GET['month']}{request.GET['year'][2:4]}_qp_{request.GET['variant']}"
    url = f"https://bestexamhelp.com/exam/cambridge-igcse/biology-0610/{request.GET['year']}/{filename}.pdf"
    print(url)
    r = requests.get(url, stream=True)
    
    # https://docs.python.org/3/library/tempfile.html
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as fd:
        for chunk in r.iter_content(2000):
            fd.write(chunk)
        os.chmod(fd.name, 0o755)
    extractQP(os.path.abspath(fd.name), fd.name)
    return HttpResponse(os.path.getsize(os.path.abspath(fd.name)))

def results(request):
    return render(request, "marker_web/results.html")