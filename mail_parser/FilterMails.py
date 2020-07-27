import re

class FilterMails:
    def __init__(self, mails=[]):
        self.mails = []
        self.add_mails(mails)


    def add_mails(self, mails):
        _ = [self.mails.extend(i) if type(i) is list else self.mails.append(i) for i in mails]

    def get_clear_unique_mails(self):
        self.filter_mails()
        self.mails = list(set(self.mails))
        return [i for i in self.mails if i]


    def filter_mails(self):
        clear_elements = []
        if self.mails:
            for i in self.mails:
                if len(i) < 100:
                    if self.isEnglish(i):
                        if not self.is_file(i):
                            if i[0] != '.' and i[-1] != '.':
                                clear_elements.extend(self.regex_mail_from_string(i))

        self.mails = clear_elements


    def isEnglish(self, s):
        return s.isascii()

    def is_file(self, url):
        black_list = ['.jpg', '.jpeg', '.png', '.svg', '.ico', '.pdf', '.txt', '.xml', '.mp3', '.mp4', '.avi']
        return bool([i for i in black_list if i in url.lower()])

    @staticmethod
    def regex_mail_from_string(string):
        if string:
            regex = r"[\w\.-]+@[\w\.-]+\.\w+"
            url = re.findall(regex, string)
            url = [i for i in url if not i[-1].isnumeric()]
            return url
