from bs4 import BeautifulSoup
from mail_parser.FilterMails import FilterMails

class GetMails:
    def __init__(self, html_instance):
        self.html_instance = html_instance
        self.mails = []
        self.urlCount = 0

    def profit_count(self):
        self.urlCount += 1
        if self.urlCount and len(self.mails):
            if self.urlCount // len(self.mails) > 200:
                print('skipped by bad profit')
                return False

        return True

    def get_mails(self, url):
        if self.profit_count():
            html = self.html_instance.get_html(url)

            if html:
                text = BeautifulSoup(html.text, 'lxml')
                all_text = text.findAll(text=True)
                elems_like_mails = [i.lower() for i in all_text if '@' in i and '.' in i if len(i) < 200]

                self.mails.extend(
                    FilterMails(elems_like_mails).get_clear_unique_mails()
                )
                self.mails = list(set(self.mails))

    def get_clean_mails(self):
        return FilterMails(self.mails).get_clear_unique_mails()




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

