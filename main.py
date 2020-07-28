from config import *
import grequests
import document
from mail_parser.GetMails import GetMails
from multiprocessing import Pool
import time
from url_parser.FilterUrls import FilterUrls
from url_parser.get_all_links import get_all_links

start_program = time.time()
domains = document.read_lines('text_files/input.txt')




def links_from_domain(domain):
    dirty_links = get_all_links(domain)
    box = FilterUrls(dirty_links)
    return box.get_validated_urls()


def multiproc(domain, step=ASYNCH_LINKS):
    urls = links_from_domain(domain)
    mails = []

    cycle = 0
    mails_result = 0
    ###счетчики
    domain_print = urls[0] if urls else None
    start_print = time.time()
    urls_print = 0
    all_urls_print = len(urls) if urls else 0
    invalid_print = 0
    ###счетчики

    if urls:
        while urls:
            urls_print += len(urls[:step])
            cycle_time = time.time()
            new_mails, invalid_print = fetch(urls[:step])

            mails_result += len(new_mails)
            cycle += 1
            urls = urls[step:]
            mails.extend(new_mails)
            mails = list(set(mails))
            print('#################################')
            if len(urls): print('осталось проверить ссылок в рамках домена', len(urls), domain_print)
            if time.time() - cycle_time > TIMEOUT_CYCLE_DOMAIN:
                if time.time() - cycle_time > TIMEOUT_CYCLE_DOMAIN * 2.5:
                    debug_info = '{}    {}'
                    document.write_lines('debug_files/bad_time.txt', [debug_info.format(time.time() - cycle_time, domain)])
                print('timeout cycle', domain_print)
                break

            if not (cycle % PROFIT_CYCLE_DOMAIN_COUNTER and cycle != 0):    # раз в X цикла проверяет результативность
                if mails_result: mails_result = 0
                else:
                    print('bad profit', domain)
                    break

        print('домен: ', domain_print)
        print('почтовиков найдено: ', len(mails), mails)
        print('времени на домен: ', time.time() - start_print)
        print('ссылок проверено: ', urls_print, 'из', all_urls_print, 'не ответили на запрос:', invalid_print)
        print('#################################')

        return mails if mails else []


def fetch(urls, timeout=TIMEOUT_GET):
    invalid_print = 0
    print(urls[0])
    GetMails_inst = GetMails()
    rs = (grequests.get(u, timeout=timeout, ) for u in urls)
    for i in grequests.map(rs):
        if i:
            GetMails_inst.get_mails(i)
        else:
            invalid_print += 1
    return GetMails_inst.get_clean_mails(), invalid_print



def printer(start, all_mails, domains, text='время работы шага'):
    print('#######################################################')
    print(f'{text}:  ', time.time() - start)
    print('почтовиков найдено:  ', all_mails)
    print('доменов проверено:  ', domains)
    print('#######################################################')



def while_by_step():
    domains = True

    _mails = 0
    _domains = 0

    while domains:
        start = time.time()
        all_mails = []

        domains = document.read_lines('text_files/input.txt')[:STEP]
        _domains += len(domains)

        with Pool(POOLS) as p:
            _ = [all_mails.extend(i) for i in p.map(multiproc, domains) if i]

        document.write_lines('text_files/mails.txt', all_mails)
        document.write_lines('debug_files/old_domains.txt', domains)
        document.cut_lines('text_files/input.txt', STEP)

        printer(start, len(all_mails), len(domains))
        _mails += len(all_mails)

    printer(start_program, _mails, domains, text='время работы программы')

if __name__ == '__main__':
    while_by_step()