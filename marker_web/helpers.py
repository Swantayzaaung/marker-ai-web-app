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

    return questions 