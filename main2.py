from bs4 import BeautifulSoup
from get_html import get_html
import threading
import time
from multiprocessing import Pool
import GetValidatedMails


# class ParseSite:
#     def __init__(self, domain):
#         self.domain = domain
#         self.validatedUrls = GetValidatedUrls(domain).get_validated_urls()
#
#     def threading(self):
#         while self.validatedUrls:
#             time.sleep(0.2)
#             print('осталось ссылок:', len(self.validatedUrls))
#             if threading.active_count() < 8:
#                 target = GetValidatedMails(self.validatedUrls.pop())
#                 x = threading.Thread(target=target.get_validated_mails)
#                 x.start()
#         with open('result.txt', 'a', encoding='utf8', newline='\n') as file:
#             [file.write(i + '\n') for i in set(validatedMails)]



def readDomains():
    with open('input2.txt', 'r') as file:
        reader = ['http://' + i for i in file.read().split('\n') if i.strip() != '']
    return reader

# def writeDomains(source):
#     with open('domains.txt', 'a', encoding='utf8', newline='\n') as file:
#         [file.write(i + '\n') for i in set(validatedMails)]



# def multiproc(url):
#     print(url)
#     target = ParseSite(url)
#     target.threading()



if __name__ == '__main__':
    # domains = readDomains()
    # with Pool(8) as p:
    #     print(p.map(multiproc, domains))
    test = GetValidatedMails()
    q = [test.add_url(i) for i in readDomains()]
    print([i for i in test.mails if i])