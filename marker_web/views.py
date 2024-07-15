from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from .helpers import createPDFzip, extractQP, extractMS

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
            "questions": questions[1:]
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
                if len(question[0]) > 2:
                    print(question[0][-1])
                else:
                    print("smth else")

            # if len(question[0]) > 0:
            #     print(f"Question is {question[0][1]}\n")

                        
        return render(request, "marker_web/results.html", {
            "normalQ": array,
            "tableQ": tableQ,
            "answers": request.POST
        })
        
    
def results(request):
    return render(request, "marker_web/results.html")