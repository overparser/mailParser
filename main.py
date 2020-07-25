from get_html import GetHtml
import document
from FilterMails import FilterMails
from FilterUrls import FilterUrls
from get_dirty_mails import get_dirty_mails
from get_all_links import get_all_links
import time

domains = document.readDomains('input2.txt')
start = time.time()
mails_counter = 0

def mails_from_url_list(url_list):
    if not url_list:
        return

    global mails_counter
    mails_counter += 1
    html_instance = GetHtml()   # инстанс для подсчета невалидных ссылок в рамках одного домена
    mail_box = FilterMails()
    print(f'счетчик доменов поиска почты: {mails_counter} \n', f'прошло времени: {time.time() - start}')

    for i in url_list:
        dirty_mails = get_dirty_mails(i, html_instance)
        mail_box.add_mails(dirty_mails)
    mail_box.filter_mails()
    return mail_box.get_clear_unique_mails()

links_counter = 0
def links_from_domain(domain):
    global links_counter
    links_counter += 1
    dirty_links = get_all_links(domain)
    box = FilterUrls(dirty_links)
    print(f'счетчик доменов ссылок: {links_counter} \n', f'прошло времени: {time.time() - start}')
    return box.get_validated_urls()


links = list(map(links_from_domain, domains))
document.writeLines('linksresult.txt', links)
mails = list(map(mails_from_url_list, links))

document.writeLines('mailresult.txt', mails)
print('конец выполнения:  ', time.time() - start)
