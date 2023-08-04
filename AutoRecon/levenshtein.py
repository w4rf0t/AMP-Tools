import Levenshtein
import asyncio
import aiohttp
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
G = "\033[32m"
B = "\033[34m"

async def multi_check(session, response1, secondEle, data):
    if secondEle < len(data):
        data2 = data[secondEle].strip()
        try:
            async with session.get(data2, timeout=5, ssl=False) as response:
                response2 = await response.text()
                if Levenshtein.ratio(response1, response2) > 0.7:
                    data.pop(secondEle)
        except:
            if secondEle < len(data):
                data.pop(secondEle)


async def check_plagiarism_sub(target):
    async with aiohttp.ClientSession() as session:
        with open(f"Result/{target}/recon/{target}_live.txt", "r") as f:
            data = f.readlines()
        firstEle = 0
        count = len(data)
        while firstEle < len(data)-1 or round((firstEle+1)/len(data)*100)<100:
            try:
                data1 = data[firstEle].strip()
                print(B,f"[*] Checking PlagiaRism...: {round((firstEle+1)/len(data)*100)} % ", end="\r")
                async with session.get(data1, timeout=5, ssl=False) as response:
                    response1 = await response.text()
                threads = []
                secondEle = firstEle
                while secondEle < len(data)-1:
                    secondEle += 1
                    threads.append(asyncio.create_task(
                        multi_check(session, response1, secondEle, data)))
                await asyncio.gather(*threads)
            except:
                # pass
                data.pop(firstEle)
            firstEle += 1
        print(G,f"[*] {count-len(data)} subdomains found PlagiaRism or cannot Access were removed 👌")
        with open(f"Result/{target}/recon/{target}_live.txt", "w") as f:
            f.writelines(data)
