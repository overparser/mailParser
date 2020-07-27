from bs4 import BeautifulSoup
from mail_parser.FilterMails import FilterMails

class GetMails:
    def __init__(self):
        self.mails = []


    def get_mails(self, html):
        if html:
            text = BeautifulSoup(html.text, 'lxml')
            all_text = text.findAll(text=True)
            elems_like_mails = [i.lower() for i in all_text if '@' in i and '.' in i if len(i) < 200]
            self.mails.extend(elems_like_mails)

    def get_clean_mails(self):
        elems_like_mails = list(set(self.mails))
        return FilterMails(elems_like_mails).get_clear_unique_mails()