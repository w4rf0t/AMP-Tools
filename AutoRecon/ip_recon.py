import os
import subprocess
import json
import re
import threading

W = "\033[0m"
R = "\033[31m"
G = "\033[32m"
O = "\033[33m"
B = "\033[34m"

def get_ip_nmap(target):
    with open(f'Result/{target}/status_of_function.json', 'r') as f:
        data=json.load(f)
    data["ip_Recon"]["get_ip_nmap"]=0
    with open(f"Result/{target}/status_of_function.json","w") as f:
        json.dump(data, f, indent=4)

    print(B,"Generating IP ports service...","\r")
    with open(f'Result/{target}/final_status_{target}.json',"r") as file1:
            datas = json.load(file1)
    IPs = []
    for data in datas:
        for key in data:
            if data[key]['host'] not in IPs:            # unique IP
                IPs.append(data[key]['host'])
    threads = []
    for ip in IPs:
        threads.append(threading.Thread(target=os.system(f"nmap -sT -sV --top-ports 1000  {ip} >> Result/{target}/{target}_ip/nmap_{ip}.txt")))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    
    pattern = r'(\d+)\/(\w+)\s+(\w+)\s+([\w\.\-\s]+?)\s*(?:\n|$)'
    regex = re.compile(pattern)
    data = []
    for ip in IPs:
        with open(f"Result/{target}/{target}_ip/nmap_{ip}.txt","r") as file3:
            text_data = file3.read()
            matches = regex.findall(text_data)
            for match in matches:
                object = { ip : { "port" : match[0], "protocol" : match[1], "service" : match[2], "version" : match[3] } }
                data.append(object)
    with open(f"Result/{target}/{target}_ip/nmap_{target}.json","a") as file4:
        json.dump(data,file4,indent=4)
    subprocess.run(f"rm -rf Result/{target}/{target}_ip/nmap_*.txt",shell=True)

    data["ip_Recon"]["get_ip_nmap"]=1
    with open(f"Result/{target}/status_of_function.json","w") as f:
        json.dump(data, f, indent=4)
        
    print(G,"Generating IP ports service done !")

def scan_input_IP(target):
    with open(f'Result/{target}/status_of_function.json', 'r') as f:
        dataf=json.load(f)
    dataf["ip_Recon"]["scan_input_IP"] = 0
    with open(f"Result/{target}/status_of_function.json","w") as f:
        json.dump(dataf, f, indent=4)
    print(B,"Generating IP ports service...","\r")
    os.system(f"nmap -sT -sV {target} >> Result/{target}/{target}_ip/nmap_{target}.txt")
    
    pattern = r'(\d+)\/(\w+)\s+(\w+)\s+([\w\.\-\s]+?)\s*(?:\n|$)'
    regex = re.compile(pattern)
    data = []
    list_WebIP = []
    with open(f"Result/{target}/{target}_ip/nmap_{target}.txt","r") as file3:
        text_data = file3.read()
    matches = regex.findall(text_data)
    for match in matches:
        object = { target : { "port" : match[0], "protocol" : match[1], "status" : match[2], "service" : match[3] } }    
        data.append(object)
        list_WebIP.append(str(target+':'+match[0]))
    with open(f"Result/{target}/{target}_ip/nmap_{target}.json","w") as file4:
        json.dump(data,file4)
    with open(f"Result/{target}/final_subdomain_{target}.txt","w") as file5:
        for ip in list_WebIP:
            file5.write(ip+"\n")
    
    command_probe = [f"cat Result/{target}/final_subdomain_{target}.txt | ~/go/bin/httprobe >>  Result/{target}/{target}_live.txt"]
    subprocess.run(command_probe, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL, shell=True)
    command_httpx = [f"cat Result/{target}/{target}_live.txt | ~/go/bin/httpx -sc -td -ip -server -nc -json -o Result/{target}/final_status_{target}.json"]
    subprocess.run(command_httpx, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL, shell=True)    

    dataf["ip_Recon"]["scan_input_IP"] = 1
    with open(f"Result/{target}/status_of_function.json","w") as f:
        json.dump(dataf, f, indent=4)
    print(G,"Generating IP ports service done !")
def ip_Recon(target):

    try:
        os.makedirs(f'Result/{target}/{target}_ip', exist_ok=True)
    except FileExistsError:
        pass
    IP_regex = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    if not IP_regex.match(target):
        get_ip_nmap(target)
    else:
        scan_input_IP(target)