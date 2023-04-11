# from threading import Thread
# import requests
import Levenshtein
import asyncio
import aiohttp 
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
G = "\033[32m"

# def multi_check(respones1,secondEle,data):
#     if secondEle < len(data):
#         data2 = data[secondEle].strip()
#         try:
#             response2 = requests.get(data2,timeout=10,verify=False).text
#             if Levenshtein.ratio(respones1,response2) > 0.9:
#                 data.pop(secondEle)
#         except:
#             if secondEle < len(data):
#                 data.pop(secondEle)

# def check_plagiarism_sub(target):
#     with open(f"Result/{target}/recon/{target}_live.txt", "r") as f:
#         data = f.readlines()
#     firstEle = 0
#     count = len(data)
#     while firstEle < len(data)-1:
#         try:
#             data1 = data[firstEle].strip()
#             print(f" Checking PlagiaRism...: {round((firstEle+1)/len(data)*100)} % ",end="\r")
#             response1 = requests.get(data1,timeout=10,verify=False).text
#             threads = []
#             secondEle = firstEle
#             while secondEle < len(data)-1:
#                 secondEle += 1
#                 threads.append(Thread(target=multi_check, args=[response1, secondEle ,data]))
#             for thread in threads:
#                 thread.start()
#             for thread in threads:
#                 thread.join()
#             # firstEle += 1
#         except:
#             pass
#             data.pop(firstEle)
#         firstEle += 1
#     with open(f"Result/{target}/recon/{target}_live.txt", "w") as f:
#         f.writelines(data)
#     print(G,f" {count-len(data)} subdomains found PlagiaRism or cannot Access were removed 👌")
    
async def multi_check(session, response1, secondEle, data):
    if secondEle < len(data):
        data2 = data[secondEle].strip()
        try:
            async with session.get(data2, timeout=15, ssl=False) as response:
                response2 = await response.text()
                if Levenshtein.ratio(response1, response2) > 0.7:
                    print(f"{data2} trung roi nha")
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
        while firstEle < len(data)-1:
            try:
                data1 = data[firstEle].strip()
                print(f" Checking PlagiaRism...: {round((firstEle+1)/len(data)*100)} % ", end="\r")
                async with session.get(data1, timeout=15, ssl=False) as response:
                    response1 = await response.text()
                threads = []
                secondEle = firstEle
                while secondEle < len(data)-1:
                    secondEle += 1
                    threads.append(asyncio.create_task(multi_check(session, response1, secondEle, data)))
                await asyncio.gather(*threads)
            except:
                # pass
                data.pop(firstEle)
            firstEle += 1
        with open(f"Result/{target}/recon/{target}_live.txt", "w") as f:
            f.writelines(data)
        print(G+f"\n {count-len(data)} subdomains found PlagiaRism or cannot Access were removed 👌")
        
