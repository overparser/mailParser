import grequests
import document
import time
start = time.time()
urls = ['http://' + i for i in document.read_lines('text_files/input2.txt')[0:10]]

rs = (grequests.get(u, timeout=33) for u in urls)

for i in grequests.map(rs):
    if i:
        print(i.text)

print(time.time() - start)