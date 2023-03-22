import json
import requests
from urllib3.exceptions import InsecureRequestWarning
import warnings
warnings.simplefilter('ignore', InsecureRequestWarning)


def getToken():
    url = "https://localhost:8834/session"
    data = {"username": "admin", "password": "kali"}
    try:
        respone = requests.post(url, data=data, verify=False)
        token = respone.json()['token']
        return str(token)
    except:
        return str(None)


def NessusScan(target):
    url = "https://localhost:8834/scans"
    token = getToken()
    headers = {
    "X-Api-Token": "0968773D-72BB-4594-B1A4-0D311FE5EA57",
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
        return respone.json()
    except:
        return str(None)

print(NessusScan("etc.vn"))