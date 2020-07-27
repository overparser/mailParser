import document
from url_parser.FilterUrls import FilterUrls
from url_parser.get_all_links import get_all_links
import time
from mail_parser.ThreadsMailsParser import ThreadsMailsParser
from multiprocessing import Pool


def links_from_domain(domain):
    dirty_links = get_all_links(domain)
    box = FilterUrls(dirty_links)
    return box.get_validated_urls()


def multiproc(domain):
    array = links_from_domain(domain)
    inst = ThreadsMailsParser(array)
    return inst.multi_threads()



def pool(threads, step):
    domains = document.cut_lines('text_files/input2.txt', step)
    while domains:
        result = []
        while_start = time.time()
        with Pool(threads) as p:
            _ = [result.extend(i) for i in p.map(multiproc, domains)]
        print(result)
        document.write_lines('text_files/mails.txt', result)
        print('########################################################################')
        print('Времени на последний цикл:  ', time.time() - while_start)
        document.write_lines('debug_files/oldDomains.txt', domains)
        domains = document.cut_lines('text_files/input2.txt', step)

def console(domains_count):
    mails_count = len((document.read_lines('text_files/mails.txt')))
    if not mails_count:
        mails_count = 1

    print('########################################################################')
    print('Время выполнения: ', time.time() - start)
    print('доменов проверено: ', domains_count)

    print('Найдено почтовых ящиков: ', mails_count)
    print('в среднем почтовых ящиков в минуту: ', mails_count // (time.time() - start) * 60)

    print('########################################################################')

if __name__ == '__main__':
    # domains_count = len(document.read_lines('text_files/input2.txt'))
    # pool(30, step=1000)
    # console(domains_count)
    print(links_from_domain('google.com/'))

