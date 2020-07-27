from urllib.parse import urljoin
import re
import time
from misc.blacklist import black_list

class FilterUrls:
    def __init__(self, urls):
        print('входящие ссылки ', len(urls), urls)
        self.set_domain(urls)
        self.urls = urls

    def get_validated_urls(self):
        if self.urls:
            self.urls = list(map(self.href_validation, self.urls))
            self.regex_filter()
            self.domain_in_url()
            result = list(set(self.urls))
            print('выходящие ссылки ', result)
            return result

    def set_domain(self, urls):
        domain = urls[0] if urls else '!!!!'
        self.domain_http = 'http://' + domain if 'http://' not in domain else domain
        self.domain_https = 'https://' + domain if 'https://' not in domain else domain

    def set_http(self, url):
        if 'http://' not in url and 'https://' not in url:
            return 'http://' + url
        return url

    def regex_filter(self):
        result = []
        for url in self.urls:
            if url:
                if len(url) > 100:  # исправить это место. Регекс зависает на строках более ~150 символов
                    result.append(url)
                    continue
                regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
                if 'http' not in url:
                    url = url.replace('//', '')
                url = re.findall(regex, url)
                urls = [x[0] for x in url]
                if urls:
                    result.extend(urls)
                    continue
                result.append(url)
                continue
            else:
                continue
        self.urls = result

    def domain_in_url(self):
        result = []
        for url in self.urls:
            if self.domain_http in url or self.domain_https in url:
                result.append(url)
        self.urls = result

    def href_validation(self, url):  # привести к нормальному виду blacklist.py/whitelist
        if not url:
            return
        if not url.isascii():
            return

        if self.is_file(url):
            return
        if '#' in url:
            return

        if '.' not in url and '/' not in url:
            return

        if ';' in url:
            return

        if 'javascript' in url:
            return

        if 'www.' not in url and 'http://' not in url and 'https://' not in url:
            url = urljoin(self.domain_http, url)

        return url



    def is_file(self, url):
        return bool([i for i in black_list if i in url.lower()])
