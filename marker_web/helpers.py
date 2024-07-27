# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

import logging, os, csv, glob, re, zipfile, json, io, spacy, numpy as np, math, textwrap
# https://developer.adobe.com/document-services/docs/overview/pdf-extract-api/howtos/extract-api/
from . import cred 
from .models import *
from compare.startup import nlp
from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import ExtractElementType
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_renditions_element_type import \
    ExtractRenditionsElementType
from adobe.pdfservices.operation.pdfops.options.extractpdf.table_structure_type import TableStructureType
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

# https://stackoverflow.com/questions/4623446/how-do-you-sort-files-numerically
def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)

# Divide string into n equal sized segments

def split_string(string, parts):
    sub_len = math.ceil(len(string)/parts)
    result = textwrap.wrap(string, sub_len)
    return result

# Remove empty elements from array
def clear_empty(array):
    return [item for item in array if item != ""]

def replace_blanks(array):
    output_arr = []
    blank_count = 0
    startIndex = -1
    
    question_no = array[0]
    sub_question = ""
    sub_index = ""
    
    for i,s in enumerate(array):
        
        if re.search(r'\.{4,}', s):
            if startIndex == -1:
                startIndex = i
            blank_count += 1
        else:
            if blank_count > 0:
                combined_string = ''.join(array[startIndex:startIndex+blank_count])
                combined_string = re.sub(r'(\.{4,}\s*)+', f'<br><textarea required class="form-control" placeholder="Enter answer for {question_no}{sub_question}{sub_index}" name="{question_no}{sub_question}{sub_index}"></textarea><br>', combined_string)
                output_arr.append(combined_string)
            output_arr.append(s)
            blank_count = 0
            startIndex = -1
            
        # Get the current number: e.g 4(a)(ii), so that I can put this in the textarea input
        if s[0] == '(':
            if re.match(r'^\([a-h]\)', s):
                # For sub questions
                sub_question = s.split(' ')[0]
                sub_index = ""
            elif re.match(r'^\([ivx]+\)', s):
                # For sub index like 1(a)(i)
                sub_index = s.split(' ')[0]
                
    if blank_count > 0:
        combined_string = ''.join(array[startIndex:startIndex+blank_count])
        combined_string = re.sub(r'(\.{4,}\s*)+', f'<br><textarea required class="form-control" placeholder="Enter answer for {question_no}{sub_question}{sub_index}" name="{question_no}{sub_question}{sub_index}"></textarea><br>', combined_string)
        output_arr.append(combined_string)   
            
    return output_arr

# Credit: https://developer.adobe.com/document-services/docs/overview/pdf-extract-api/howtos/extract-api/
def createPDFzip(filepath, filename):
    try:
        # get base path.
        input_pdf = os.path.join(filepath, filename)

        # Initial setup, create credentials instance.
        credentials = Credentials.service_principal_credentials_builder(). \
            with_client_id(cred.PDF_SERVICES_CLIENT_ID). \
            with_client_secret(cred.PDF_SERVICES_CLIENT_SECRET). \
            build()

        # Create an ExecutionContext using credentials and create a new operation instance.
        execution_context = ExecutionContext.create(credentials)
        extract_pdf_operation = ExtractPDFOperation.create_new()

        # Set operation input from a source file.
        source = FileRef.create_from_local_file(input_pdf)
        extract_pdf_operation.set_input(source)

        # Build ExtractPDF options and set them into the operation
        extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
            .with_elements_to_extract([ExtractElementType.TEXT, ExtractElementType.TABLES]) \
            .with_element_to_extract_renditions(ExtractRenditionsElementType.TABLES) \
            .with_table_structure_format(TableStructureType.CSV) \
            .build()
        extract_pdf_operation.set_options(extract_pdf_options)

        # Execute the operation.
        result: FileRef = extract_pdf_operation.execute(execution_context)

        # Save the result to the specified location.
        result.save_as(f"{filename}.zip")
    except (ServiceApiException, ServiceUsageException, SdkException):
        logging.exception("Exception encountered while executing operation")
        
def extractQP(filepath):
    archive = zipfile.ZipFile(filepath, 'r')
    jsonentry = archive.open('structuredData.json')
    jsondata = jsonentry.read()
    data = json.loads(jsondata)
    questions = []
    question = []
    index=1
    currentNum = ""
    for i in range(len(data["elements"])):
        if 'Text' in data['elements'][i]:
            currentText = data['elements'][i]["Text"].strip()
            try:
                nextText = data["elements"][i+1]["Text"].strip()
            except:
                nextText = ""

            # Split the text up into different question numbers
            if len(currentText) == 1 or currentText.split(" ")[0] == str(index):
                if nextText != "":
                    if nextText.strip()[0] != '.':
                        if currentText == str(index):
                            index+=1
                            if question != []:
                                questions.append(replace_blanks(question)[1:])
                                # questions.append(question)
                                question = []
            question.append(currentText)

    questions.append(replace_blanks(question)[1:])
    # questions.append(question)

    # Add line breaks to text input boxes and single words
    for question in questions:
        for i in range(len(question)):
            if question[i][0] == '(':
                question[i] = "<br>" + question[i]
            elif question[i][-1] == ']':
                question[i] = question[i] + "<br>"

    # Remove any stuff that comes after the last question ends (e.g BLANK PAGE texts)
    lastIndex = 0
    for item in questions[-1]:
        if ']' in item:
            lastIndex = questions[-1].index(item) + 1
    questions[-1][lastIndex:] = [""] * (len(questions[-1]) - lastIndex)

    return questions

# def isSubNumber(element):
#     if element.

def extractMS(filepath):
    # Credit: https://johnvastola.medium.com/how-to-combine-multiple-csv-files-using-python-to-analyze-797fc825c541
    archive = zipfile.ZipFile(filepath, 'r')
    all_files = archive.namelist()
    csv_files = [file for file in all_files if file.endswith('.csv')]
    sort_nicely(csv_files)

    # Use a wildcard pattern to match all CSV files in the directory
    # Initialize an empty list to store rows from each file
    normalQ = []
    tableQ = []
    # Read and append rows from each CSV file to the normalQ list
    for file in csv_files:
        with archive.open(file) as csvfile:
            text = io.TextIOWrapper(csvfile, encoding='utf-8-sig')
            reader = csv.reader(text)
            header = next(reader)
            if 'Question' in header[0]:
                if not normalQ:  # Include header only once
                    normalQ.append(list(filter(None, header)))
                # normalQ.extend(row for row in reader)
                for row in reader:
                    currentRow = [item.strip() for item in row]
                    try:
                        nextRow = [item.strip() for item in next(reader)]
                        # https://www.geeksforgeeks.org/remove-empty-elements-from-an-array-in-javascript/
                        if nextRow[0] == '':
                            tableQ.append(currentRow)
                            tableQ.append(nextRow)     
                        else:
                            normalQ.append(clear_empty(currentRow))                   
                            normalQ.append(clear_empty(nextRow))                 
                    except:
                        normalQ.append(clear_empty(currentRow))
        
    # for x in normalQ:
    #     array = x
    #     print(array[1])
    return normalQ, tableQ
    
    
# Credit to Otto Sukpraput :))
""" This model only compares word vectors"""
def word2vec_calculate_similarity(response, markscheme):
    # Tokenize and get Word2Vec vectors for each token
    response_vectors = [token.vector for token in nlp(response) if not token.is_stop and not token.is_punct]
    markscheme_vectors = [token.vector for token in nlp(markscheme) if not token.is_stop and not token.is_punct]
    # If either of the vectors is empty, return a low similarity score
    if not response_vectors or not markscheme_vectors:
        return 0.0

     # Calculate the cosine similarity between the vectors
    similarity_score = np.dot(np.sum(response_vectors, axis=0), np.sum(markscheme_vectors, axis=0))
    response_norm = np.linalg.norm(np.sum(response_vectors, axis=0))
    markscheme_norm = np.linalg.norm(np.sum(markscheme_vectors, axis=0))
    # Normalize the similarity score to be in range [-1, 1]
    if response_norm > 0 and markscheme_norm > 0:
        similarity_score /= (response_norm * markscheme_norm)

    return similarity_score


""" model_used can take in 1 2 or 3, 1 = word2vec, 2 = use, 3 = both"""
def output_mark(response, markscheme, word2vec_threshold=0.7):
    word2vec_similarity_score = 0 
    word2vec_similarity_score = round(float(word2vec_calculate_similarity(response, markscheme)), 1)
    # print(type(word2vec_similarity_score))
    # print("Word2vec (threshold: {}): {}".format(word2vec_threshold, word2vec_similarity_score))
    return word2vec_similarity_score > word2vec_threshold

""" For each point given by the student, compare it against each markscheme point which have not been used and award a mark if they are similar
 If a mark is awarded (or more), return a list of indexes in markscheme_point used
 Note: 1 point can be awarded multiple marks """
def mark_per_point(student_point, markscheme, correct_points, indexes_not_allowed):
    marks = 0
    for i in range(len(markscheme)):
        if i not in indexes_not_allowed:
            # print("\nYour point: {}".format(student_point), end=" || ")
            # print(markscheme[i])
            if output_mark(student_point, markscheme[i]):
                marks += 1
                indexes_not_allowed.append(i)
                # print("Marks +1")
                correct_points[i] = True
            # else:
                # print("Marks +0")
    return marks
