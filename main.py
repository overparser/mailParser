from get_html import GetHtml
import document
from FilterUrls import FilterUrls
from get_all_links import get_all_links
import time
from MailsFromDomainUrls import MailsFromDomainUrls
from multiprocessing import Pool

domains = document.readDomains('input2.txt')
start = time.time()
mails_counter = 0



links_counter = 0
def links_from_domain(domain):
    global links_counter
    links_counter += 1
    dirty_links = get_all_links(domain)
    box = FilterUrls(dirty_links)
    print(f'счетчик доменов ссылок: {links_counter} \n', f'прошло времени: {time.time() - start}')
    return box.get_validated_urls()


# domains = list(map(links_from_domain, domains))

result = []
# for domain in domains:
#     inst = MailsFromDomainUrls(domain)
#     result.extend(inst.multi_threads())

# document.writeLines('mails.txt', result)


def multiproc(domain):
    array = links_from_domain(domain)
    inst = MailsFromDomainUrls(array)
    print(time.time() - start)
    return inst.multi_threads()

if __name__ == '__main__':
    result = []
    with Pool(20) as p:
        _ = [result.extend(i) for i in p.map(multiproc, domains)]
    print(result)
    document.writeLines('mails.txt', result)
    print(time.time() - start)
