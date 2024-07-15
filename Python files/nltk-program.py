import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

string = 'Any three from:  Use a firewall Use of a proxy server Do not use / download software / files from unknown sources  Do not share external storage devices / USB pens Do not open / take care when opening attachments / link Do not connect computer to network / use as stand-alone computer Limiting access to the computer  '

print(sent_tokenize(string))
