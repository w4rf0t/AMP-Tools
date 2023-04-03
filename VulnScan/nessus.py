import json
import os
import re
from termcolor import colored
import time
import requests
from urllib3.exceptions import InsecureRequestWarning
import warnings
warnings.simplefilter('ignore', InsecureRequestWarning)
W = "\033[0m"
R = "\033[31m"
G = "\033[32m"
O = "\033[33m"
B = "\033[34m"

def logo():
    os.system("clear")
    print(colored('''
╔╗╔┌─┐┌─┐┌─┐┬ ┬┌─┐  ╔═╗┌─┐┌─┐┌┐┌
║║║├┤ └─┐└─┐│ │└─┐  ╚═╗│  ├─┤│││
╝╚╝└─┘└─┘└─┘└─┘└─┘  ╚═╝└─┘┴ ┴┘└┘''',"red"))

def get_X_API_Token():
    url = "https://127.0.0.1:8834/nessus6.js"
    response = requests.get(url, verify=False).text
    pattern = r"return\"(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})\""
    matches = re.findall(pattern, response)
    return matches[1]


def getToken():
    url = "https://127.0.0.1:8834/session"
    data = {"username": "admin", "password": "kali"}
    try:
        respone = requests.post(url, data=data, verify=False)
        token = respone.json()['token']
        return str(token)
    except:
        return str(None)


def Scan(target,x_api_token,token):
    url = "https://127.0.0.1:8834/scans"
    headers = {
        "X-Api-Token": x_api_token,
        "X-Cookie": "token=" + token + "",
        "Content-Type": "application/json",
        "Content-Length": "295"
    }
    data = {
        "uuid": "ab4bacd2-05f6-425c-9d79-3ba3940ad1c24e51e1f403febe40",
        "settings": {
        "emails": "hkphu.edu@gmail.com",
        "attach_report": "yes",
        "filter_type": "and",
        "launch_now": "true",
        "enabled": "false",
        "name": "Scan Policy of AMP for "+target,
        "folder_id": 3,
        "scanner_id": "1",
        "policy_id": "4",
        "text_targets": target,
        "file_targets": ""
    }
    }
    try:
        data = json.dumps(data)
        respone = requests.post(url, headers=headers, data=data, verify=False)
        return str(respone.json()['scan']['id'])
    except:
        return str(None)

def checkStatus(target,idscan,x_api_token,token):
    url = f"https://127.0.0.1:8834/scans/{idscan}?limit=2500&includeHostDetailsForHostDiscovery=true"
    headers = {
        "X-Api-Token": x_api_token,
        "X-Cookie": "token=" + token + "",
        "Content-Type": "application/json"
    }
    try:
        respone = requests.get(url, headers=headers, verify=False)
        res = json.loads(respone.content)
        with open(f'Result/{target}/NessusScan/{target}_status.json', 'w') as f:
            json.dump(res, f, indent=4)
        return res["hosts"][0]["scanprogresscurrent"],res["info"]["status"]
    except:
        return 0,res["info"]["status"]

def getFileToken(idscan,x_api_token,token):
    url = "https://127.0.0.1:8834/scans/" + str(idscan) + "/export?limit=2500"
    headers = {
        "X-Api-Token": x_api_token,
        "X-Cookie": "token=" + token + "",
        "Content-Type": "application/json",
        "Content-Length": "295"
    }
    data ={"format":"pdf","template_id":46,"csvColumns":{},"formattingOptions":{"page_breaks":"false"},"extraFilters":{"host_ids":[],"plugin_ids":[]}}
    try:
        data = json.dumps(data)
        respone = requests.post(url, headers=headers, data=data, verify=False)
        token = respone.json()['token']
        return str(token)
    except:
        return str(None)
    
def exportFile(target,idscan):
    token = getToken()
    x_api_token = get_X_API_Token()
    fileToken=getFileToken(idscan,x_api_token,token)
    time.sleep(5)
    print("File token: " +fileToken)
    url = f'https://127.0.0.1:8834/tokens/{fileToken}/download'
    headers = {
            "X-Api-Token": x_api_token,
            "X-Cookie": "token=" + token + "",
        }
    response = requests.get(url, headers=headers ,verify=False)
    with open(f'Result/{target}/NessusScan/{target}.pdf', 'wb') as f:#,encoding='utf-8'
        f.write(response.content)
    
def NessusScan(target):
    logo()
    startTime = time.time()
    token = getToken()
    x_api_token = get_X_API_Token()
    idscan = int(Scan(target,x_api_token,token)) # idscan = "131"
    scanProgress,status = checkStatus(target,idscan,x_api_token,token)
    if status == "completed":
        print(G,"Done Scaning Nessus !!!")
    else:
        while status != "completed":
            time.sleep(5)
            if (time.time() - startTime) % 1200 == 0:
                x_api_token = get_X_API_Token()
            scanProgress,status = checkStatus(target,idscan,x_api_token,token)
            for char in ["|", "/", "-", "\\"]:
                print(B,f"Nessus {status} {scanProgress}%...{char}", end="\r")
                time.sleep(0.1)
        print(G,"\nDone Scaning Nessus !!!")
    if not os.path.exists(f"Result/{target}/NessusScan"):
        os.makedirs(f"Result/{target}/NessusScan")
    print(B,"Generating report...",end='\r')
    exportFile(target,idscan)
    print(G,"Generating report completed !!!")