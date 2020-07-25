from bs4 import BeautifulSoup

class GetDirtyMails:
    def __init__(self, html_instance):
        self.html_instance = html_instance
        self.all_dirty_mails = []

    def place_dirty_mails(self, url):
        html = self.html_instance.get_html(url)
        if html:
            text = BeautifulSoup(html.text, 'lxml')
            allText = text.findAll(text=True)
            elements_like_mails = [i for i in allText if '@' in i and '.' in i if len(i) < 200]
            self.all_dirty_mails.extend(elements_like_mails)


# def getMailsWithThreads(urls):
#     target = GetValidatedMails()
#     if len(urls) > 2000:
#         urls = urls[0:2000]
#
#
#     threads = []
#     while urls or threading.active_count() > 1:
#         if threading.active_count() < 6 and urls:
#             x = threading.Thread(target=target.get_mails, args=(urls.pop(0),))
#             x.start()
#             threads.append(x)
#         else:
#             x.join()
#         time.sleep(0.05)
#         if threading.active_count() < 6:
#             print(len(urls))
#     mails = target.get_validated_mails()
#     document.writeLines('mails.txt', mails)

