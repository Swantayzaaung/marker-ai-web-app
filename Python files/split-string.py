import math, textwrap 
string = "abcdefghijaaaaa"
def split_string(string, parts):
    sub_len = math.ceil(len(string)/parts)
    result = textwrap.wrap(string, sub_len)
    return result
print(split_string(string, 4))

