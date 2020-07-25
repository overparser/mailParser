from bs4 import BeautifulSoup

def get_dirty_mails(url, html_instance):
    html = html_instance.get_html(url)
    if html:
        text = BeautifulSoup(html.text, 'lxml')
        allText = text.findAll(text=True)
        elements_like_mails = [i for i in allText if '@' in i and '.' in i if len(i) < 200]

        return elements_like_mails
    else:
        return []




















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

