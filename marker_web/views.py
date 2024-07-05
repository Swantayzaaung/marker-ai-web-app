from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from .helpers import createPDFzip, extractQP

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
    # try:
    #     filename = f"{request.GET['subject'].split('-')[-1]}_{request.GET['month']}{request.GET['year'][2:4]}_qp_{request.GET['variant']}"
    #     url = f"https://bestexamhelp.com/exam/cambridge-igcse/{request.GET['subject']}/{request.GET['year']}/{filename}.pdf"
    #     print(url)
    #     r = requests.get(url, stream=True)
        
    #     # https://docs.python.org/3/library/tempfile.html
    #     with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as fd:
    #         for chunk in r.iter_content(2000):
    #             fd.write(chunk)
    #         os.chmod(fd.name, 0o755)
    #     print(tempfile.gettempdir()) 
    #     createPDFzip(tempfile.gettempdir(), fd.name)
    #     # Once you get the zip file, open the damn thing and show the contents on the webpage
    #     questions = extractQP(os.path.join(tempfile.gettempdir(), fd.name + ".zip"))
    #     return render(request, "marker_web/practice.html", {
    #         "questions": questions
    #     })
    # except:
    #     return HttpResponse("file not found")
    path = os.path.join(os.path.abspath(os.getcwd()), 'marker_web', '0610_s19_qp_43.zip')
    print(path)
    questions = extractQP(path)
    return render(request, "marker_web/practice.html", {
        "questions": questions[1:]
    })
    
def results(request):
    return render(request, "marker_web/results.html")