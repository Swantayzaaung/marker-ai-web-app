from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from .helpers import createPDFzip, extractQP, extractMS, split_string, mark_per_point
from django.views.decorators.csrf import csrf_exempt

import requests, tempfile, os, json

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
        
@csrf_exempt
def results(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        all_data = []
        MSpath = os.path.join(os.path.abspath(os.getcwd()), 'marker_web', 'bio m19 ms 42.zip')
        normalQ, tableQ = extractMS(MSpath)
        for key in list(data.keys())[1:]:
            answer = []
            question = [row for row in normalQ if row[0] == key][0]
            if len(question) > 0:
                if len(question[0]) > 2:
                    max_marks = int(question[2])
                mark_scheme_points = [q for q in question[1].split(';') if q != ""]
                correct_points = [False for i in range(len(mark_scheme_points))]
                # print(mark_scheme_points)
                if type(data[key]) == list:
                    for item in data[key]:
                        answer.extend(item.split('.'))
                else:
                    answer = data[key].split('.')
                print(answer)
                
                indexes_not_allowed = [] # passed by ref
                marks = 0
                for point in answer:
                    marks += mark_per_point(point, mark_scheme_points, correct_points, indexes_not_allowed)
                    if marks >= max_marks:
                        break
                print("Total marks: {}".format(marks))
                
                marked_data = {
                    "mark_scheme_points": mark_scheme_points,
                    "correct_points": correct_points, 
                    "marks": marks
                }
                
                all_data.append(marked_data)

                # if len(question[0]) > 0:
                #     print(f"Question is {question[0][1]}\n")
        return JsonResponse({
            "all_data": all_data
        })