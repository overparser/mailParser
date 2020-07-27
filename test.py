import grequests
import time
from main import links_from_domain
import document
from mail_parser.GetMails import GetMails
from multiprocessing import Pool, cpu_count, active_children
from multiprocessing import Process
import time



start_program = time.time()
domains = document.read_lines('text_files/input2.txt')




def multiproc(domain, step=20):
    urls = links_from_domain(domain)
    mails = []
    cycle = 0
    mails_result = 0
    domain_print = urls[0] if urls else None
    print(domain_print)
    start_print = time.time()
    urls_print = 0
    all_urls_print = len(urls) if urls else 0
    invalid_print = 0
    if urls:
        while urls:
            urls_print += len(urls[:step])
            cycle_time = time.time()
            new_mails, invalid_print = thread(urls[:step])
            mails_result += len(new_mails)
            cycle += 1
            urls = urls[step:]
            mails.extend(new_mails)
            mails = list(set(mails))

            print('#################################')
            if len(urls): print('осталось проверить ссылок в рамках домена', len(urls), domain_print)

            if time.time() - cycle_time > 10:
                print('timeout cycle', domain_print)
                break

            if not (cycle % 5 and cycle != 0):
                if mails_result: mails_result = 0
                else:
                    print('timeout cycle')
                    break

        print('домен: ', domain_print)
        print('почтовиков найдено: ', len(mails), mails)
        print('времени на домен: ', time.time() - start_print)
        print('ссылок проверено: ', urls_print, 'из', all_urls_print, 'из них невалидных', invalid_print)
        print('#################################')

        return mails if mails else []


def thread(urls, timeout=8):
    invalid_print = 0
    print(urls[0])
    GetMails_inst = GetMails()
    rs = (grequests.get(u, timeout=3, ) for u in urls)
    for i in grequests.map(rs, gtimeout=timeout):
        if i:
            GetMails_inst.get_mails(i)
        else:
            invalid_print += 1
    return GetMails_inst.get_clean_mails(), invalid_print



def multi_threads(domains, threads=8):
    counter = len(domains)
    while domains:
        domain = domains[0]
        counter -= 1
        while len(active_children()) >= threads:
            time.sleep(0.5)
            print(len(active_children()))

        Process(target=multiproc, args=(domain,)).start()

    return None



if __name__ == '__main__':
    start = time.time()
    # multi_threads(domains)
    # print('время работы программы:  ', time.time() - start)
    # print('время работы программы:  ', time.time() - start)
    # print('время работы программы:  ', time.time() - start)
    result = []
    with Pool(15) as p:
        _ = [result.extend(i) for i in p.map(multiproc, domains) if i]
    document.write_lines('text_files/mails.txt', result)

    print('#######################################################')
    print('время работы программы:  ', time.time() - start)
    print('почтовиков найдено:  ', len(result))
    print('доменов проверено:  ', len(domains))





#     print('почтовиков найдено: ', len(result))
# print('время работы программы:  ', time.time() - start_program)
