import requests, tempfile, os

url = 'https://bestexamhelp.com/exam/cambridge-igcse/biology-0610/2021/0610_m21_qp_42.pdf'
r = requests.get(url, stream=True)

with tempfile.NamedTemporaryFile() as fd:
    for chunk in r.iter_content(2000):
        fd.write(chunk)
    print(os.path.getsize(fd.name))
   


        