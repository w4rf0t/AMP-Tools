import json
import os
import re
import time
import requests
from urllib3.exceptions import InsecureRequestWarning
import warnings
warnings.simplefilter('ignore', InsecureRequestWarning)


def get_X_API_Token():
    url = "https://localhost:8834/nessus6.js"
    response = requests.get(url, verify=False).text
    pattern = r"return\"(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})\""
    matches = re.findall(pattern, response)
    return matches[1]


def getToken():
    url = "https://localhost:8834/session"
    data = {"username": "admin", "password": "kali"}
    try:
        respone = requests.post(url, data=data, verify=False)
        token = respone.json()['token']
        return str(token)
    except:
        return str(None)


def Scan(target,x_api_token,token):
    url = "https://localhost:8834/scans"
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
        "name": target,
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

def checkStatus(idscan,x_api_token,token):
    url = f"https://localhost:8834/scans/{idscan}?limit=2500&includeHostDetailsForHostDiscovery=true"
    headers = {
        "X-Api-Token": x_api_token,
        "X-Cookie": "token=" + token + "",
        "Content-Type": "application/json",
        "Content-Length": "295"
    }
    try:
        respone = requests.get(url, headers=headers, verify=False)
        return respone.json()['host']['scanprogresscurrent']
    except:
        return 100

def getFileToken(idscan,x_api_token,token):
    url = "https://localhost:8834/scans/" + str(idscan) + "/export?limit=2500"
    headers = {
        "X-Api-Token": x_api_token,
        "X-Cookie": "token=" + token + "",
        "Content-Type": "application/json",
        "Content-Length": "295"
    }
    data ={"format":"pdf","template_id":1156,"csvColumns":{},"formattingOptions":{"page_breaks":"false"},"extraFilters":{"host_ids":[],"plugin_ids":[]}}
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
    url = f'https://localhost:8834/tokens/{fileToken}/download'
    headers = {
            "X-Api-Token": x_api_token,
            "X-Cookie": "token=" + token + "",
        }
    response = requests.get(url, headers=headers ,verify=False)
    with open(f'Result/{target}/NessusScan/{target}.pdf', 'wb') as f:
        f.write(response.content)
    
def NessusScan(target):
    token = getToken()
    x_api_token = get_X_API_Token()
    idscan = "131"
    # idscan = Scan(target,x_api_token,token)
    scanProgress = checkStatus(idscan,x_api_token,token)
    if scanProgress == 100:
        print("Done Scaning Nessus !!!")
    else:
        while scanProgress <= 100:
            scanProgress = checkStatus(idscan,x_api_token,token)
            for char in ["|", "/", "-", "\\"]:
                print(f"Nessus scaning {scanProgress}%...{char}", end="\r")
                time.sleep(0.1)
        print("Done Scaning Nessus !!!")
    try:
        os.system(f"mkdir Result/{target}/NessusScan")
    except:
        pass
    print("Generating report...")
    exportFile(target,idscan)
    