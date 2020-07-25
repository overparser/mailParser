import re


def findLinks(string):
    if string:
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        if 'http' not in string:
            string = string.replace('//', '')
        url = re.findall(regex, string)
        urls = [x[0] for x in url]
        if urls:
            return urls[0]
        return string
    else:
        return []

def findMails(string):
    if string:
        regex = r"[\w\.-]+@[\w\.-]+\.\w+"
        url = re.findall(regex, string)
        url = [i for i in url if not i[-1].isnumeric()]
        return url