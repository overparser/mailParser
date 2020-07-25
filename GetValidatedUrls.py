from bs4 import BeautifulSoup
from document import readDomains
from urllib.parse import urljoin
from urllib.parse import quote
from get_html import GetHtml
import document
from linkValidator import findLinks
from GetValidatedMails import getMailsWithThreads
from multiprocessing import Pool
import time


start = int(time.time())

class GetValidatedUrls:
    def __init__(self, domain):
        self.domain = domain

    def get_validated_urls(self):
        hrefs = self.get_all_href(self.domain)
        validatedHrefList = list(map(self.href_validation, hrefs))
        clearUrls = list(set(i for i in validatedHrefList if i))
        clearUrls.insert(0, self.domain)
        return clearUrls

    def get_all_href(self, url):
        html = GetHtml()
        html = html.get_html(url)
        if html:
            soup = BeautifulSoup(html.text, 'lxml')
            urls = soup.findAll('a')
            urls = [i.get('href') for i in urls]
            urls = [i.replace(' ', quote(' ')) if ' ' in i else i for i in urls if i]
            return urls
        return []

    def url_is_file(self, url):
        url = url.lower()
        if '.jpg' in url:
            return True
        if '.jpeg' in url:
            return True
        if '.png' in url:
            return True
        if '.svg' in url:
            return True
        if '.ico' in url:
            return True
        if '.pdf' in url:
            return True
        if '.txt' in url:
            return True
        if '.xml' in url:
            return True

    def href_validation(self, url):
        if url is None:
            return

        if self.url_is_file(url):
            return

        if '#' in url:
            return

        if 'javascript' in url:
            return

        url = findLinks(url)

        if 'www' in url or 'http' in url:
            return url
        else:
            if ':' in url:
                return
            if self.domain in url:
                return url
            domain = 'http://' + self.domain
            return urljoin(domain, url)


domains = readDomains('input2.txt')
# for i in domains:
#     test = GetValidatedUrls(i)
#     list_ = test.get_validated_urls()
#     getMailsWithThreads(list_)
#     document.writeLines('testData.txt', list_)
#     list_ = []

def multiproc(url):
    test = GetValidatedUrls(url)
    list_ = test.get_validated_urls()
    getMailsWithThreads(list_)



if __name__ == '__main__':
    with Pool(20) as p:
        p.map(multiproc, domains)
    # while domains:
    #     print(len(domains), 'site count')
    #     multiproc(domains.pop(0))

print(time.time() - start)
