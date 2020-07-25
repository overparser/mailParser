from get_html import GetHtml
from bs4 import BeautifulSoup
import document
import threading
import time
from linkValidator import findMails




class GetValidatedMails:
    def __init__(self):
        self.html = GetHtml()
        self.dirtyMails = []
        self.mails = []


    def get_validated_mails(self):
        self.mails = list(set(self.mails))
        return [i for i in self.mails if i]

    def isEnglish(self, s):
        return s.isascii()


    def is_file(self, url):
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

    def doValidate(self, elements):
        clearElements = []
        for i in elements:
            if self.isEnglish(i):
                if not self.is_file(i):
                    if i[0] != '.' and i[-1] != '.':
                        clearElements.append(i)
        return clearElements



    def get_mails(self, url):
        html = self.html.get_html(url)
        if html:
            text = BeautifulSoup(html.text, 'lxml')
            allText = text.findAll(text=True)

            elementsLikemails = [i for i in allText if '@' in i and '.' in i]
            elementsLikemails = self.doValidate(elementsLikemails)

            for i in elementsLikemails:
                self.mails.extend(findMails(i))
        else:
            return []


def getMailsWithThreads(urls):
    target = GetValidatedMails()
    if len(urls) > 2000:
        urls = urls[0:2000]


    threads = []
    while urls or threading.active_count() > 1:
        if threading.active_count() < 6 and urls:
            x = threading.Thread(target=target.get_mails, args=(urls.pop(0),))
            x.start()
            threads.append(x)
        else:
            x.join()
        time.sleep(0.05)
        if threading.active_count() < 6:
            print(len(urls))
    mails = target.get_validated_mails()
    document.writeLines('mails.txt', mails)

