import subprocess
import os
import json
import requests
from AutoRecon.module.load_config import *
from AutoRecon.module.check_ip import *
from AutoRecon.module.scidr import *

W = "\033[0m"
R = "\033[31m"
G = "\033[32m"
O = "\033[33m"
B = "\033[34m"


def recon_sub(target, dataf):
    print(B,'[*] Enumerating subdomain...', end="\r")
    dataf["Sub_Recon"]["call_subfinder"] = "0"
    with open(f"Result/{target}/status_of_function.json", "w") as f:
        json.dump(dataf, f, indent=4)
    # Passive
    try: call_scidr(target) 
    except: pass
    try: call_subfinder(target)
    except: pass
    try: call_securitytrails(target)
    except: pass
    
    dataf["Sub_Recon"]["call_subfinder"] = "1"
    with open(f"Result/{target}/status_of_function.json", "w") as f:
        json.dump(dataf, f, indent=4)
        
def call_subfinder(target):
    subfinder_command = f"subfinder -d {target} -silent -all -o Result/{target}/recon/subdomain_{target}_subfinder.txt"
    process = subprocess.Popen(subfinder_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    
def call_securitytrails(target): 
    config=load_config()
    securitrails_api_key=config.get('securitrails_api_key') 
    if securitrails_api_key =="":
        securitrails_api_key = input("Please enter your Securitytrails_Api_Key: ")
        config['securitrails_api_key'] = securitrails_api_key
        
    url = "https://api.securitytrails.com/v1/domain/{}/subdomains".format(
            target)
    headers = {
        "apikey": f"{securitrails_api_key}"
        }
    response = requests.get(url, headers=headers,timeout=10)
    subdomains = set()
    response_json = response.json()
    for subdomain in response_json["subdomains"]:
        full_subdomain = f"{subdomain}.{target}"
        subdomains.add(full_subdomain)
    with open(f"Result/{target}/recon/subdomain_{target}_securitytrails.txt", "a") as f:
        for subdomain in subdomains:
            f.write("%s\n" % subdomain)

            
def call_scidr(target):
    scidr(target)

def sanitize_input(target):
    os.system(f"cat Result/{target}/recon/subdomain_{target}_subfinder.txt >> Result/{target}/recon/subdomain_{target}.txt;rm Result/{target}/recon/subdomain_{target}_subfinder.txt ")
    os.system(f"cat Result/{target}/recon/subdomain_{target}_securitytrails.txt >> Result/{target}/recon/subdomain_{target}.txt;rm Result/{target}/recon/subdomain_{target}_securitytrails.txt ")
    os.system(f"cat Result/{target}/recon/subdomain_{target}_scidr.txt >> Result/{target}/recon/subdomain_{target}.txt;rm Result/{target}/recon/subdomain_{target}_scidr.txt ")
    os.system(f"awk '!seen[$0]++' Result/{target}/recon/subdomain_{target}.txt > Result/{target}/recon/final_subdomain_{target}.txt; rm Result/{target}/recon/subdomain_{target}.txt ")

    command_probe = [
        f"cat Result/{target}/recon/final_subdomain_{target}.txt | httprobe >>  Result/{target}/recon/{target}_live.txt"]
    subprocess.run(command_probe, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True)

    command_httpx = [
        f"cat Result/{target}/recon/{target}_live.txt | httpx -sc -td -ip -server -nc -json -o Result/{target}/recon/final_status_{target}.json"]
    subprocess.run(command_httpx, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True)

    with open(f'Result/{target}/recon/final_status_{target}.json', 'r') as f:
        contents = f.readlines()
    with open(f'Result/{target}/recon/{target}_RESULT.json', 'w') as clgt:
        clgt.write('[\n')
        for i in contents:
            i = i.strip()
            clgt.write(i + ',\n')
        clgt.seek(clgt.tell()-2, os.SEEK_SET)
        clgt.write('\n]')
    subprocess.call(f'rm -f Result/{target}/recon/final_status_{target}.json',
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    with open(f'Result/{target}/recon/{target}_RESULT.json', 'r') as f:
        datas = json.load(f)
    finaldata = []
    for data in datas:
        host = data['host']
        port = data['port']
        scheme = data['scheme']
        url=data['url']
        try:
            tech = data['tech']
        except:
            tech = None
        try:
            title = data['title']
        except:
            title = None
        object = {data['url'].split("//")[1].split(":")[0]: {'url':url,'host': host,
                                                             'port': port, 'scheme': scheme, 'tech': tech, 'title': title}}
        finaldata.append(object)
    with open(f'Result/{target}/recon/final_status_{target}.json', 'w', encoding='utf-8') as f:
        json.dump(finaldata, f, indent=4, ensure_ascii=False)
    subprocess.call(f'rm -f Result/{target}/recon/{target}_RESULT.json',
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

def sub_Recon(target):
    with open(f'Result/{target}/status_of_function.json', 'r') as f:
        dataf = json.load(f)
        recon_sub(target, dataf)
    dataf["Sub_Recon"]["sanitize_input"] = "0"
    with open(f"Result/{target}/status_of_function.json", "w") as f:
        json.dump(dataf, f, indent=4)
    sanitize_input(target)
    dataf["Sub_Recon"]["sanitize_input"] = "1"
    with open(f"Result/{target}/status_of_function.json", "w") as f:
        json.dump(dataf, f, indent=4)
    print(G,"[*] Enumerating subdomain done !")
