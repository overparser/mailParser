from fake_useragent import UserAgent
import requests
from document import writeLine
from document import readDomains
import time

ua = UserAgent()
userAgent = {'User-Agent': ua.chrome}
proxy = {
    "http": "http://tuthixen-dest:53d8tl329rrx@45.95.96.237:80",
    "https": "https://tuthixen-dest:53d8tl329rrx@45.95.96.237:80"
}

with open('proxies.txt', 'r') as file:
    proxies = file.read().split('\n')

def get_proxy():
    proxy = proxies.pop(0)
    proxies.append(proxy)
    proxy = {
    "http": f"http://{proxy}",
    "https": f"https://{proxy}"
    }
    return proxy



class GetHtml:
    def __init__(self):
        self.errorCounter = 0
        self.session = requests.Session()
        self.session.headers = userAgent
        self.session.proxies = ''

    def domain_counter(self):
        self.errorCounter += 1
        print('error counter: ', self.errorCounter)



    def statusCodeProcedure(self, status_code, url):
        self.domain_counter()
        if status_code == 404:
            return False

        if status_code == 500:
            self.session.proxies = get_proxy()
            try:
                return self.session.get(url, timeout=4)
            except:
                return 500


    def get_html(self, url):
        if self.errorCounter < 15:
            if 'http://' not in url and 'https://' not in url:
                url = 'http://' + url
            try:
                r = self.session.get(url, timeout=3)

            except:
                self.domain_counter()
                writeLine('timeOutLinks.txt', f'{url}')
                return False
            i = 0
            status = r.status_code
            while status != 200:
                r = self.statusCodeProcedure(status, url)
                i += 1
                if i > 10 or not r:
                    self.domain_counter()
                    writeLine('wrongStatusCode.txt', f'{status} {url}')
                    return False
            return r
        return False