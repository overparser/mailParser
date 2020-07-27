from get_html import GetHtml
from mail_parser.FilterMails import FilterMails
import time
import threading
from mail_parser.GetMails import GetMails


class ThreadsMailsParser:
    def __init__(self, url_list):
        if not url_list:
            url_list = []

        self.url_list = url_list
        self.start = time.time()
        self.html_instance = GetHtml()  # инстанс для подсчета невалидных ссылок в рамках одного домена
        self.get_mails_inst = GetMails()  # инстанс для снятия элементов похожих на почту

    def one_thread(self):
        url_list = self.url_list
        get_mails_inst = self.get_mails_inst
        counter = len(url_list)
        for url in url_list:
            self.console(url, counter)
            get_mails_inst.get_mails(url)

        dirty_mails = get_mails_inst.mails
        return FilterMails(dirty_mails).get_clear_unique_mails()

    @staticmethod
    def console(url, counter):
        counter -= 1
        print('запущено потоков: ', threading.active_count() - 1,
              'осталось ссылок: ', counter,
              'url:  ', url)

    def multi_threads(self, threads=10):
        threads = threads + 1
        url_list = self.url_list
        counter = len(url_list)
        get_mails_inst = self.get_mails_inst

        # if len(url_list) > 200:
        #     url_list = url_list[:200]

        for url in url_list:
            counter -= 1
            self.console(url, counter)
            while threading.active_count() >= threads:
                time.sleep(0.5)

            if threading.active_count() < threads:
                threading.Thread(target=get_mails_inst.get_mails, args=(url,)).start()

        return get_mails_inst.mails

