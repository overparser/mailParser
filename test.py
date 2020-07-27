import grequests
import time
from main import links_from_domain
import document
from mail_parser.GetMails import GetMails
from multiprocessing import Pool, cpu_count
import time



start_program = time.time()
domains = document.read_lines('text_files/input2.txt')


def multiproc(domain):
    nons = []
    counter_all_links = 0
    counter_all_valid_links = 0
    start = time.time()
    urls = links_from_domain(domain)
    GetMails_inst = GetMails()

    if urls:
        urls = urls if len(urls) < 200 else urls[:200]
        print(len(urls))
        len_urls = len(urls) if(len(urls)) > 10 else 20  # греквест может бесконечно обрабатывать некоторые сайты, например uebot.niu.edu
        len_urls = len_urls if len_urls < 40 else 40  # максимальный таймаут
        result = []
        rs = (grequests.get(u, timeout=3, ) for u in urls)
        for i in grequests.map(rs, gtimeout=len_urls):
            if i:
                print(i.status_code)
                result.append(i)
                GetMails_inst.get_mails(i)
            else:
                nons.append(i)
        mails = GetMails_inst.get_clean_mails()
        print('#############################')
        if result:
            if result[0]:
                print('ссылка  :', result[0].url)
        print('timeout:  ', len_urls)
        print(len(nons), 'ошибок')
        print(len(urls), 'ссылок')
        print(len(urls) - len(nons), 'валидных ссылок')
        print('время работы цикла:  ', time.time() - start)
        print('почтовиков найдено: ', len(mails), mails)
        counter_all_links += len(urls)
        counter_all_valid_links += len(urls) - len(nons)
        print('всего ссылок было проверено', counter_all_links)
        print('всего валидных ссылок получено', counter_all_valid_links)
        print('#############################')
        return mails



if __name__ == '__main__':
    result = []
    with Pool(1) as p:
        _ = [result.extend(i) for i in p.map(multiproc, domains) if i]
    document.write_lines('text_files/mails.txt', result)
    print('почтовиков найдено: ', len(result))
print('время работы программы:  ', time.time() - start_program)
