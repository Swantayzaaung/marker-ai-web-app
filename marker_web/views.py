from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import File, ContentFile
from .helpers import createPDFzip, extractQP, extractMS, split_string, mark_per_point
from .models import *


import requests, tempfile, os, json

# Create your views here.


def index(request):
    return render(request, "marker_web/index.html")

def about(request):
    return render(request, "marker_web/about.html")

def practice(request):
    # https://stackoverflow.com/questions/34503412/download-and-save-pdf-file-with-python-requests-module
    if request.method == "GET":
        subject = request.GET['subject'].split('_')
        year = request.GET['year']
        month = request.GET['month'].split('_')
        variant = request.GET['variant']
        longfilename = f"{subject[0].capitalize()} {year} {month[0]} {variant}"
        filename = f"{subject[1]}_{month[1]}{year[2:4]}_qp_{variant}"
        url = f"https://bestexamhelp.com/exam/cambridge-igcse/{subject[0]}-{subject[1]}/{year}/{filename}.pdf"
        if DownloadedPaper.objects.filter(filename=f"{filename}.zip").exists():
            QPpath = DownloadedPaper.objects.get(filename=f"{filename}.zip").file.path
            questions, img_lists = extractQP(QPpath)
        else:
            r = requests.get(url, stream=True)
            
            # https://docs.python.org/3/library/tempfile.html
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as fd:
                for chunk in r.iter_content(2000):
                    fd.write(chunk)
                os.chmod(fd.name, 0o755)
            createPDFzip(tempfile.gettempdir(), fd.name)

            QPpath = os.path.join(tempfile.gettempdir(), fd.name + ".zip")
            questions, img_lists = extractQP(QPpath)
            
            # Create new downloaded paper instance in DB
            newPaper = DownloadedPaper(filename=f"{filename}.zip")
            newPaper.save()
            with open(QPpath, 'rb') as f:
                newPaper.file.save(f"{filename}.zip", File(f), save=True)
        
        # for x in (questions):
            # print(x)
        return render(request, "marker_web/practice.html", {
            "questions": zip(questions[1:], img_lists[1:]),
            "longfilename": longfilename,
            "filename": filename.replace("qp", "ms"),
            "url": url.replace("qp", "ms"),

        })
        
@csrf_exempt
def results(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Download MS if the zip file doesn't exist yet
        
        all_data = []
        filename = data["ms"].split(' ')[0]
        url = data["ms"].split(' ')[1]
        if DownloadedPaper.objects.filter(filename=f"{filename}.zip").exists():
            # Load MS data and compare answers
            MSpath = DownloadedPaper.objects.get(filename=f"{filename}.zip").file.path
        else:
            r = requests.get(url, stream=True)
            
            # https://docs.python.org/3/library/tempfile.html
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as fd:
                for chunk in r.iter_content(2000):
                    fd.write(chunk)
                os.chmod(fd.name, 0o755)
            createPDFzip(tempfile.gettempdir(), fd.name)

            MSpath = os.path.join(tempfile.gettempdir(), fd.name + ".zip")
            
            # Create new downloaded paper instance in DB
            newPaper = DownloadedPaper(filename=f"{filename}.zip")
            newPaper.save()
            with open(MSpath, 'rb') as f:
                newPaper.file.save(f"{filename}.zip", File(f), save=True)
        
        normalQ, tableQ = extractMS(MSpath)
        for key in list(data.keys())[2:]:
            answer = []
            question = [row for row in normalQ if row[0] == key]
            print(question)
            print(data[key])
            if len(question) > 0:
                question = question[0]
                max_marks = 0
                if len(question[0]) > 2:
                    max_marks = int(question[2])
                mark_scheme_points = [q for q in question[1].split(';') if q != ""]
                correct_points = [False for i in range(len(mark_scheme_points))]
                if type(data[key]) == list:
                    for item in data[key]:
                        answer.extend(item.split('.'))
                else:
                    answer = data[key].split('.')
                
                indexes_not_allowed = [] # passed by ref
                marks = 0
                for point in answer:
                    marks += mark_per_point(point, mark_scheme_points, correct_points, indexes_not_allowed)
                    if marks >= max_marks:
                        break
                
                marked_data = {
                    "num": key,
                    "mark_scheme_points": mark_scheme_points,
                    "correct_points": correct_points, 
                    "got_marks": marks,
                    "max_marks": max_marks
                }
                
                all_data.append(marked_data)

        return JsonResponse({
            "all_data": all_data
        })
