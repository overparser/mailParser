import requests
from bs4 import BeautifulSoup
import csv
from fake_useragent import UserAgent
import time


domain = 'https://www.sph.umn.edu/'

ua = UserAgent()
userAgent = {'User-Agent': ua.chrome}
proxy = {
    "http": "http://tuthixen-dest:53d8tl329rrx@45.95.96.237:80",
    "https": "https://tuthixen-dest:53d8tl329rrx@45.95.96.237:80"
}


def get_html(url):
    try:
        r = requests.get(url, userAgent)
    except:
        r = requests.get('https://www.google.com/', userAgent)
        print(url)
    i = 0
    while r.status_code != 200 and i < 10:
        r = requests.get(url, userAgent)
        i += 1
        print('status code != 200')
    return r


def get_all_href(url):
    soup = BeautifulSoup(get_html(url).text, 'lxml')
    urls = soup.findAll('a')
    urls = [i.get('href') for i in urls]
    return urls


def href_validation(domain, url):
    if url == None:
        return
    if '#' in url:
        return

    if 'www' in url or 'http' in url:
        return url
    else:
        return (domain + '/' + url).replace('//', '/').replace('//', '/').replace(':/', '://')

def mailValidation(mail):
    mail = mail.strip()

    if len(mail) > 20:
        return

    splitDots = mail.split('.')
    if len(splitDots) > 2:
        return
    if not len(splitDots[0]) or not len(splitDots[1]):
        return

    splitDogs = mail.split('@')
    if len(splitDogs) > 2:
        return
    if not len(splitDogs[0]) or not len(splitDogs[1]):
        return

    return mail


def get_mails(url):
    text = BeautifulSoup(get_html(url).text, 'lxml')
    alltext = text.findAll(text=True)
    mails = [i.strip() for i in alltext if '@' in i and '.' in i]
    return mails


def readDomains(path):
    with open(path, 'r', encoding='utf8') as file:
        reader = [i[0] for i in csv.reader(file)]
    return reader

if __name__ == '__main__':
    a = readDomains('input2.txt')

    urls = get_all_href(domain)
    validUrls = [domain]
    print(urls)
    for url in urls:
        validUrls.append(href_validation(domain, url))
    validUrls = list(set(validUrls))
    print('найдено ссылок: ', len(validUrls))

    mails = []
    for url in validUrls:
        mails.extend(get_mails(url))
        print(validUrls.index(url), url)
    mails = list(set(mails))
    validMail = []

    for mail in mails:
        validMail.append(mailValidation(mail))
    validMail = [i for i in validMail if i]
    print(validMail)
    print(len(validMail))
