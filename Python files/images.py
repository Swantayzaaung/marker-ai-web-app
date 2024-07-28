import zipfile, json, os
filepath = os.path.abspath('./0610_m18_qp_42.zip')
archive = zipfile.ZipFile(filepath, 'r')
jsonentry = archive.open('structuredData.json')
jsondata = jsonentry.read()
data = json.loads(jsondata)
for i in range(len(data["elements"])):
    if 'filePaths' in data['elements'][i]:
        fp = data['elements'][i]['filePaths']
        for path in fp:
            if path.endswith('png'):
                needed_path = (os.path.join(filepath + ' pictures', path))
                if os.path.exists(needed_path):
                    print("already exist")
                else:
                    archive.extract(path, filepath + ' pictures')
                    print("extracted",path)
                
                