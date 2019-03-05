from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""
    a = a.split("\n")
    b = b.split("\n")
    c = list()
    for string in a:
        if string in b and string not in c:
            c.append(string)
    return c


def sentences(a, b):
    """Return sentences in both a and b"""
    a = sent_tokenize(a, language='english')
    b = sent_tokenize(b, language='english')
    c = list()
    for string in a:
        if string in b and string not in c:
            c.append(string)
    return c


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    a = getsubstring(a, n)
    b = getsubstring(b, n)
    c = list()
    for string in a:
        if string in b and string not in c:
            c.append(string)
    return c


def getsubstring(string, n):
    """ Function to create substrings"""
    substring = []
    if n > len(string):
        return []
    while len(string) / n >= 1:
        substring.append(string[0:n])
        string = string[1:]
    return substring
