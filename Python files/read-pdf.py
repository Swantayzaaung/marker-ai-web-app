import zipfile
import json

zip_file = "./output/adobe-extract-ms-text.zip"
archive = zipfile.ZipFile(zip_file, 'r')
jsonentry = archive.open('structuredData.json')
jsondata = jsonentry.read()
data = json.loads(jsondata)

for element in data["elements"]:
    if "Text" in element:
        print(element["Text"])