import asyncio
from aiohttp import ClientSession
import document
import time
import async_timeout

domains = document.read_lines('text_files/input2.txt')
domains = ['http://' + i for i in domains]

start = time.time()


async def fetch(url, session):
    try:
        async with session.get(url, timeout=30) as response:
            delay = response.headers.get("content-type")
            date = response.headers.get("content-length")
            print("{}:{} with delay {}".format(date, response.url, delay))
            return await response.read()
    except:
        print('None')
        return None


async def bound_fetch(url, sem, session):
    # Getter function with semaphore.
    async with sem:
        await fetch(url, session)


async def run():
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(300)

    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession() as session:
        for i in domains:
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch(i, sem, session))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        await responses

number = 10000
loop = asyncio.get_event_loop()

future = asyncio.ensure_future(run())
loop.run_until_complete(future)

print(time.time() - start)
