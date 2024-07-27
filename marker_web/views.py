from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import File
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
        print(f"Filename: {filename}")
        print(f"Long Filename: {longfilename}")
        if DownloadedPaper.objects.filter(filename=f"{filename}.zip").exists():
            QPpath = DownloadedPaper.objects.get(filename=f"{filename}.zip").file.path
            questions = extractQP(QPpath)
        else:
            url = f"https://bestexamhelp.com/exam/cambridge-igcse/{subject[0]}-{subject[1]}/{year}/{filename}.pdf"
            r = requests.get(url, stream=True)
            print("URL is", url)
            
            # https://docs.python.org/3/library/tempfile.html
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as fd:
                for chunk in r.iter_content(2000):
                    fd.write(chunk)
                os.chmod(fd.name, 0o755)
            createPDFzip(tempfile.gettempdir(), fd.name)
            # print("amogus",os.path.join(tempfile.gettempdir(), fd.name + ".zip"))
            questions = extractQP(os.path.join(tempfile.gettempdir(), fd.name + ".zip"))
 
            # Once you get the zip file, open the damn thing and show the contents on the webpage
            QPpath = os.path.join(tempfile.gettempdir(), fd.name + ".zip")
            newPaper = DownloadedPaper.objects.create(filename=f"{filename}.zip")
            newPaper.save()
            with open(QPpath) as f:
                newPaper.file.save(f"{filename}.zip", File(f))
            # fd.delete()
        
        return render(request, "marker_web/practice.html", {
            "questions": questions[1:],
            "filename": longfilename
        })
        
        questions = extractQP(QPfile.file.path, QPfile.filename)
        return render(request, "marker_web/practice.html", {
            "questions": questions[1:],
            "filename": longfilename
        })
@csrf_exempt
def results(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        all_data = []
        MSpath = DownloadedPaper.objects.get(filename="0610_m19_ms_42").file.path
        normalQ, tableQ = extractMS(MSpath)
        for key in list(data.keys())[1:]:
            answer = []
            question = [row for row in normalQ if row[0] == key][0]
            if len(question) > 0:
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