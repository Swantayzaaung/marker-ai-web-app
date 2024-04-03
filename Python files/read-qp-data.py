""" 
Extract data:
-text questions separated according to question number
-convert ........ lines into an input => if the lines have dots in it, put them all into one line/variable to use for later
-accoutn for tables that provide information, calculation questions, questions that involve filling in tables
"""

import json
import os
import zipfile

filepath="output/0610_s19_qp_43.zip"
archive = zipfile.ZipFile(filepath, 'r')
jsonentry = archive.open('structuredData.json')
jsondata = jsonentry.read()
data = json.loads(jsondata)
questions = []
question = []
index=1
for element in data["elements"]:
    if "Text" in element:
        element["Text"] = element["Text"].strip()
        if len(element["Text"]) == 1 and element["Text"] == str(index):
            if question != []:
                questions.append(question)
                question = []
            index+=1
        question.append(element["Text"])
questions.append(question)

for question in questions:
    print(question)
    print("\033[1;31m"+"-"*30 + "\033[;37m")