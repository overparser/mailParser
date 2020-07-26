from get_html import GetHtml
from bs4 import  BeautifulSoup
from urllib.parse import quote


def get_all_links(url):
    html = GetHtml()
    html = html.get_html(url)
    if html:
        soup = BeautifulSoup(html.text, 'lxml')
        urls = soup.findAll('a')
        urls = [i.get('href') for i in urls]
        urls = [i.replace(' ', quote(' ')) if ' ' in i else i for i in urls if i]   # заменяет пробелы на %20
        urls.insert(0, url)     # ставит домен первым в списке для дальнейшей проверки
        return urls
    return []

