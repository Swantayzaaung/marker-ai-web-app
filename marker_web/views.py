from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from .helpers import createPDFzip, extractQP, extractMS, split_string, mark_per_point
from compare.startup import nlp

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
    if request.method == "GET":
        longfilename = f"{request.GET['subject'].split('-')[0]}, {request.GET['year'].split('-')[0]}, {request.GET['month'].split('-')[0]}, {request.GET['variant']}"
        """try:
            filename = f"{request.GET['subject'].split('-')[-1]}_{request.GET['month']}{request.GET['year'][2:4]}_qp_{request.GET['variant']}"
            url = f"https://bestexamhelp.com/exam/cambridge-igcse/{request.GET['subject']}/{request.GET['year']}/{filename}.pdf"
            print(url)
            r = requests.get(url, stream=True)
            
            # https://docs.python.org/3/library/tempfile.html
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as fd:
                for chunk in r.iter_content(2000):
                    fd.write(chunk)
                os.chmod(fd.name, 0o755)
            print(tempfile.gettempdir()) 
            createPDFzip(tempfile.gettempdir(), fd.name)
            # Once you get the zip file, open the damn thing and show the contents on the webpage
            questions = extractQP(os.path.join(tempfile.gettempdir(), fd.name + ".zip"))
            return render(request, "marker_web/practice.html", {
                "questions": questions[1:]
            })
        except:
            return HttpResponse("file not found")"""
        QPpath = os.path.join(os.path.abspath(os.getcwd()), 'marker_web', 'bio m19 qp 42.zip')
        print(QPpath)
        questions = extractQP(QPpath)
        
        return render(request, "marker_web/practice.html", {
            "questions": questions[1:],
            "filename": longfilename
        })
    elif request.method == "POST":
        MSpath = os.path.join(os.path.abspath(os.getcwd()), 'marker_web', 'bio m19 ms 42.zip')
        normalQ, tableQ = extractMS(MSpath)
        array = []
        numbers = list(request.POST.keys())
        print(numbers)
        # print('1' in normalQ[1])
        for key in numbers:
            question = [row for row in normalQ if row[0] == key]
            if len(question) > 0:
                array.append(question)
                #print(question[0][1], end="")
                max_marks = -1
                if len(question[0]) > 2:
                    if not question[0][2]:
                        max_marks = 2
                    else:
                        max_marks = int(question[0][2])
                else:
                    max_marks = 2
                print(max_marks)
                mark_scheme_points = question[0][1].split(';')
                print(mark_scheme_points)
                student_response = request.POST[key]
                student_response_by_point = student_response.split('.')

                indexes_not_allowed = [] # passed by ref
                marks = 0
                for point in student_response_by_point:
                    marks += mark_per_point(point, mark_scheme_points, indexes_not_allowed)
                    if marks >= max_marks:
                        break
                print("Total marks: {}".format(marks))

            # if len(question[0]) > 0:
            #     print(f"Question is {question[0][1]}\n")

                        
        return render(request, "marker_web/results.html", {
            "normalQ": array,
            "tableQ": tableQ,
            "answers": request.POST
        })
        
    
def results(request):
    return render(request, "marker_web/results.html")
