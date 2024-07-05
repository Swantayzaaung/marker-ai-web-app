# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

import logging, os, csv, glob, re, zipfile, json
from . import cred 
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

def replace_blanks(array):
    output_arr = []
    blank_count = 0
    startIndex = -1
    
    currentLetter = ""
    currentNum = ""
    
    for i in range(len(array)):
        # Add line breaks in front of section markers like 2 (a), (iii), etc
        if array[i][0] == '(':
            # Get the current number: e.g 4(a)(ii)
            if re.match(r'\(([a-h])\)',array[i]):
                currentLetter = f"{array[0]}{array[i]}"[0:4]
                currentNum = currentLetter
            else:
                currentNum = currentLetter + array[i].split(' ')[0]
            print("Current number is:", currentNum)
            print("Array: ", array)
            print()
            array[i] = "<br>" + array[i]
            
        if re.search(r'\.{4,}', array[i]):
            if startIndex == -1:
                startIndex = i
            blank_count += 1
        else:
            if blank_count > 0:
                combined_string = ''.join(array[startIndex:startIndex+blank_count])
                combined_string = re.sub(r'(\.{4,}\s*)+', f'<br><textarea placeholder="Enter answer for {currentNum}"></textarea><br>', combined_string)
                output_arr.append(combined_string)
            output_arr.append(array[i])
            blank_count = 0
            startIndex = -1
    return output_arr

def createPDFzip(filepath, filename):
    try:
        # get base path.
        input_pdf = os.path.join(filepath, filename)
        print(input_pdf)
        print(os.path.getsize(input_pdf))

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
            if len(currentText) == 1:
                if nextText.strip()[0] != '.':
                    if currentText == str(index):
                        index+=1
                        if question != []:
                            questions.append(replace_blanks(question))
                            question = []
                           
            question.append(currentText)

    questions.append(replace_blanks(question))
    
    # Remove any stuff that comes after the last question ends (e.g BLANK PAGE texts)
    lastIndex = 0
    for item in questions[-1]:
        if ']' in item:
            lastIndex = questions[-1].index(item) + 1
    questions[-1][lastIndex:] = [""] * (len(questions[-1]) - lastIndex)

    return questions

# def isSubNumber(element):
#     if element.

def extractMS():
    # https://johnvastola.medium.com/how-to-combine-multiple-csv-files-using-python-to-analyze-797fc825c541

    filepath = "./output/bio ms csv/tables/"
    csv_files = glob.glob(filepath + "*.csv")
    sort_nicely(csv_files)

    # Use a wildcard pattern to match all CSV files in the directory
    # Initialize an empty list to store rows from each file
    combined_data = []
    tableQ = []
    # Read and append rows from each CSV file to the combined_data list
    for file in csv_files:
        with open(file, 'r', encoding="utf-8-sig") as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
            # print(header)
            if 'Question' in header[0]:
                if not combined_data:  # Include header only once
                    combined_data.append(list(filter(None, header)))
                # combined_data.extend(row for row in reader)
                for row in reader:
                    try:
                        nextRow = next(reader)
                        if nextRow[0] == '':
                            tableQ.append(row)
                            tableQ.append(nextRow)     
                        else:
                            combined_data.append(row)                   
                            combined_data.append(nextRow)                   
                    except:
                        combined_data.append(row)                   
        
    for row in combined_data:
        # row.pop()
        print(row)
        
    for row in tableQ:
        print(row)