import aiohttp
import asyncio
from timeit import default_timer as timer


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main(urls):
    thread_times = []
 

    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for url in urls:
            t1 = timer()
            task = asyncio.create_task(fetch(session, url))
            tasks.append(task)

        results = await asyncio.gather(*tasks)

        t2 = timer()
        for i, result in enumerate(results):

            t = t2 - t1
            thread_times.append((t2,t1))
            print(f"Thread {i+1} Time: {t}")
        
    return results, thread_times, t2 - t1

def as_request(input_file):

    with open(input_file) as file:
        urls = file.readlines()

    t1 = timer()
    result, thread_time, total_time = asyncio.run(main(urls))
    t2 = timer()
    return result, t2-t1

