from document import readDomains
from urllib.parse import urljoin
import re


class FilterUrls:
    def __init__(self, urls):
        if urls:
            self.domain = urls[0]
        else:
            self.domain = '!!!'

        self.urls = urls

    def get_validated_urls(self):
        if self.urls:
            self.href_validation()
            self.regex_filter()
            self.domain_in_url()
            return self.urls

    def regex_filter(self):
        result = []
        for url in self.urls:
            if url:
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
            if self.domain in url:
                result.append(url)
        self.urls = result


    def href_validation(self):
        result = []
        for url in self.urls:
            if not url:
                continue

            if self.is_file(url):
                continue

            if '#' in url:
                continue

            if 'javascript' in url:
                continue

            if 'www' in url or 'http' in url:
                result.append(url)
                continue
            else:
                if ':' in url:
                    continue
                if self.domain in url:
                    result.append(url)
                    continue
                domain = 'http://' + self.domain
                result.append(urljoin(domain, url))
        self.urls = result



    def is_file(self, url):
        url = url.lower()
        if '.jpg' in url:
            return True
        if '.jpeg' in url:
            return True
        if '.png' in url:
            return True
        if '.svg' in url:
            return True
        if '.ico' in url:
            return True
        if '.pdf' in url:
            return True
        if '.txt' in url:
            return True
        if '.xml' in url:
            return True