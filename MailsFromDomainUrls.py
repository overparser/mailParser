from get_html import GetHtml
from FilterMails import FilterMails
import time
import threading
from get_dirty_mails import GetDirtyMails


class MailsFromDomainUrls:
    def __init__(self, url_list, threads=10):
        if not url_list:
            url_list = []

        self.url_list = url_list
        self.threads = threads + 1
        self.start = time.time()
        self.dom_counter = 0
        self.html_instance = GetHtml()  # инстанс для подсчета невалидных ссылок в рамках одного домена
        self.dirty_mails_inst = GetDirtyMails(self.html_instance)   # инстанс для снятия элементов похожих на почту


    def multi_threads(self):
        url_list = self.url_list
        dirty_mails_inst = self.dirty_mails_inst
        counter = len(url_list)
        for url in url_list:
            counter -= 1
            print('запущено потоков: ', threading.active_count() -1,
                  'осталось ссылок: ', counter,
                  'url:  ', url)

            while threading.active_count() >= self.threads:
                time.sleep(0.5)

            if threading.active_count() < self.threads:
                    threading.Thread(target=dirty_mails_inst.place_dirty_mails, args=(url,)).start()

        dirty_mails = dirty_mails_inst.all_dirty_mails

        return FilterMails(dirty_mails).get_clear_unique_mails()



    # def one_thread(self):
    #     url_list = self.url_list
    #
    #     if not url_list:
    #         return
    #
    #     self.dom_counter += 1
    #     print(f'доменов проверено на наличие почты: {self.dom_counter} \n',
    #           f'прошло времени: {time.time() - self.start}')
    #
    #     for i in url_list:
    #         dirty_mails = get_dirty_mails(i, self.html_instance)
    #         self.mail_box.add_mails(dirty_mails)
    #     self.mail_box.filter_mails()
    #     return self.mail_box.get_clear_unique_mails()