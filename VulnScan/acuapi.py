import json
import os
import random
import subprocess
from termcolor import colored
import time
import requests
from urllib3.exceptions import InsecureRequestWarning
import warnings
warnings.simplefilter('ignore', InsecureRequestWarning)



def menu():
    subprocess.call('clear', shell=True)
    colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
    color_index = 0
    banner ='''
    _                ___ _ 
   /_\  __ _  _ __ _| _ (_)
  / _ \/ _| || / _` |  _/ |     AcuPi v1.0 from AMP Team ❤️
 /_/ \_\__|\_,_\__,_|_| |_|
    '''
    for line in banner.split('\n'):
        colored_line = ''
        for char in line:
            if char != ' ':
                colored_line += colored(char, colors[color_index % len(colors)])
                color_index += 1
            else:
                colored_line += ' '
        print(colored_line)
        

def get_X_Auth(url_acunetix):
    url = url_acunetix + "me/login"
    data = {"email": "admin@gmail.com", "password": "b03ddf3ca2e714a6548e7495e2a03f5e824eaac9837cd7f159c67b90fb4b7342", "remember_me": "false"}
    try:
        respone = requests.post(url, data=json.dumps(data), verify=False)
        token = respone.headers['X-Auth']
        return str(token)
    except:
        return str(None)

def get_target_id(url_acunetix,address,x_auth):
    headers = {"X-Auth": x_auth,"content-type": "application/json"}
    url= url_acunetix + "targets/add"
    data = {"targets":[{"address":"{}".format(address),"description":"AMP scan for {}".format(address)}],"groups":[]}
    try:
        respone = requests.post(url, headers=headers, data=json.dumps(data), timeout=30, verify=False)
        return str(json.loads(respone.content)['targets'][0]['target_id'])
    except:
        pass
def scan_target(url_acunetix,target_id,x_auth,scan_profile_id,scan_speed):
    headers = {"X-Auth": x_auth,"Content-Type": "application/json","Cookie": "ui_session={}".format(x_auth)}
    url=url_acunetix + "targets/{}/configuration".format(target_id)
    data = {"scan_speed":scan_speed,"login":{"kind":"none"},"ssh_credentials":{"kind":"none"},"default_scanning_profile_id":"11111111-1111-1111-1111-111111111111","sensor":"false","case_sensitive":"no","limit_crawler_scope":"true","excluded_paths":[],"authentication":{"enabled":"false"},"proxy":{"enabled":"false"},"technologies":[],"custom_headers":[],"custom_cookies":[],"ad_blocker":"true","debug":"false","skip_login_form":"false","restrict_scans_to_import_files":"false","issue_tracker_id":"","preseed_mode":""}
    try:
        res = requests.patch(url,data=json.dumps(data),headers=headers,timeout=30*4,verify=False)
        data = {"profile_id":scan_profile_id,"ui_session_id":"c9696e2eb2b52744bbc61e3f47dd20ec","incremental":"false","schedule":{"disable":"false","time_sensitive":"false"},"report_template_id":"11111111-1111-1111-1111-111111111111","target_id":"{}".format(target_id)}
        try:
            response = requests.post(url_acunetix + "scans", headers=headers, data=json.dumps(data),timeout=30, verify=False)
            return str(response.json()["scan_id"])
        except:
            return str(None)
    except:
        return str(None)
def get_session_id(url_acunetix,scan_id,x_auth):
    headers = {"X-Auth": x_auth,"Cookie": "ui_session={}".format(x_auth),"Referer": "https://192.168.44.128:3443/"}
    url=url_acunetix + "scans/{}".format(scan_id)
    try:
        time.sleep(1)
        response = requests.get(url, headers=headers,timeout=30, verify=False)
        session_id = json.loads(response.content)["current_session"]["scan_session_id"]
        return str(session_id)
    except:
        pass
    
def show_scan_status(url_acunetix,scan_id,session_id,x_auth,folder_name):
    headers = {"X-Auth": x_auth,"content-type": "application/json"}
    url=url_acunetix + "scans/{}/results/{}/statistics".format(scan_id,session_id)
    res = requests.get(url, headers=headers,timeout=30, verify=False)
    with open(folder_name+"/scan_status.json","w") as f:
        json.dump(json.loads(res.content),f,indent=4)
    progress = json.loads(res.content)['scanning_app']['wvs']['main']['progress']
    status = json.loads(res.content)['status']
    return progress,status

def get_vuln_info(url_acunetix,scan_id,session_id,x_auth,folder_name):
    headers = {"X-Auth": x_auth,"content-type": "application/json"}
    url=url_acunetix + "scans/{}/results/{}/vulnerabilities".format(scan_id,session_id)
    res = requests.get(url, headers=headers,timeout=30, verify=False)
    with open(folder_name+"/vuln_status.json","w") as f:
        json.dump(json.loads(res.content),f,indent=4)
    
def get_reportID(url_acunetix,session_id,x_auth):
    headers = {"X-Auth": x_auth,"Content-Type": "application/json","Cookie": "ui_session={}".format(x_auth)}
    url=url_acunetix + "reports"
    data = {"template_id":"11111111-1111-1111-1111-111111111111","source":{"list_type":"scan_result","id_list":["{}".format(session_id)]}}
    res = requests.post(url, headers=headers, data=json.dumps(data),timeout=30, verify=False)
    return json.loads(res.content)["report_id"]

def export_report(url_acunetix,report_id,x_auth,folder_name):
    download_link = str(None)
    while download_link == str(None):
        try:
            headers = {"X-Auth": x_auth,"Content-Type": "application/json","Cookie": "ui_session={}".format(x_auth)}
            download_objects = json.loads(requests.get(url_acunetix+"reports",headers=headers,timeout=30, verify=False).content)['reports']
            for i in range(len(download_objects)):
                if download_objects[i]["report_id"] == report_id:
                    download_link = download_objects[i]['download'][1]
        except:
            download_link = str(None)
    download_link = download_link.replace("/api/v1/","")
    url=url_acunetix + download_link
    with open(folder_name+"/Final_report.pdf","wb") as f:
        headers = {"X-Auth": x_auth,"content-type": "application/json"}
        url=url_acunetix + download_link
        res = requests.get(url, headers=headers,timeout=30, verify=False)
        f.write(res.content)    
    
def main(url_acunetix,x_auth,target,scan_profile_id,scan_speed,folder_name):
    # x_auth = get_X_Auth()
    # while x_auth == "None":
    #     x_auth = get_X_Auth()
    target_id = get_target_id(url_acunetix,target,x_auth)
    scan_id = scan_target(url_acunetix,target_id,x_auth,scan_profile_id,scan_speed)
    startTime = time.time()
    session_id = get_session_id(url_acunetix,scan_id,x_auth)
    time.sleep(1)
    progress, status = show_scan_status(url_acunetix,scan_id,session_id,x_auth,folder_name)
    colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
    while True:
        running_time = round(time.time() - startTime)
        if running_time%500==0:
            session_id = get_session_id(url_acunetix,scan_id,x_auth)
        if running_time%5==0:
            progress, status = show_scan_status(url_acunetix,scan_id,session_id,x_auth,folder_name)
            get_vuln_info(url_acunetix,scan_id,session_id,x_auth,folder_name)
            if status != "processing":
                break
        for char in ["\\", "|", "/", "-"]:
            print(colored("Scanning... {}%\t".format(progress),"white") + colored("{} ".format(char),colors[random.randint(0, 4)]), end="\r")
            time.sleep(0.1)
    print(colored("Downloading report...","blue"), end="\r")
    reportID = get_reportID(url_acunetix,session_id,x_auth)
    time.sleep(2)
    export_report(url_acunetix,reportID,x_auth)
    print(colored("Report downloaded successfully!","green"))
    

    
def Acunetix(target):
    try:
        menu()
        # create "result/target/vuln/acuapi" folder
        folder_name = "Result/" + target+"/AcuaPi"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        url_acunetix = "https://192.168.44.143:3443/api/v1/"
        x_auth = "1986ad8c0a5b3df4d7028d5f3c06e936ce6e15aafcc9144aeaa02df4c5b481b4b"
        scan_speed_list = {1:"sequential",2:"slow",3:"moderate",4:"fast"}
        scan_profile_list = {1:["11111111-1111-1111-1111-111111111111","Full Scan"],2:["11111111-1111-1111-1111-111111111112","High Risk Vulnerabilities"],3:["11111111-1111-1111-1111-111111111113","SQL Injection Vulnerabilities"],4:["11111111-1111-1111-1111-111111111114",'Continuous_full'],5:["11111111-1111-1111-1111-111111111115","Weak Passwords"],6:["11111111-1111-1111-1111-111111111116","Cross-site Scripting Vulnerabilities"],7:["11111111-1111-1111-1111-111111111117","Crawl Only"],8:["11111111-1111-1111-1111-111111111118","Continuous_quick"]}
        for i in range(1,5):
            print(colored("{}. {}".format(i,scan_speed_list[i]),"white"))
        print(colored("Input scan speed (1-4): ","blue"),end="")
        scan_speed = scan_speed_list[int(input())]
        for i in range(1,9):
            print(colored("{}. {}".format(i,scan_profile_list[i][1]),"white"))
        print(colored("Input scan profile (1-8): ","blue"),end="")
        scan_profile_id = scan_profile_list[int(input())][0]
        main(url_acunetix,x_auth,target,scan_profile_id,scan_speed,folder_name)
    except KeyboardInterrupt:
        print(colored("KeyboardInterrupt","red"))