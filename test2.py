import requests
import document
from main import links_from_domain
import time


domains = document.read_lines('text_files/input2.txt')
start = time.time()
def create_task(domain):
    print(domain)
    urls = links_from_domain(domain)
    print(urls)
    print(len(urls))
    rs = (requests.get(u, timeout=3) for u in urls)
    for i in rs:
        print(i)

list(map(create_task, domains))
print(time.time() - start)