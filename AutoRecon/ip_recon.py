import os
import subprocess
import sys
import json
import re
import threading

# def remove_line_regex(file_name, regex_list, ):
#     lines = open(file_name).readlines()
#     lines = [line for line in lines if not any(re.search(regex, line) for regex in regex_list)]
#     open(file_name, 'w').writelines(lines)

def get_ip_nmap(target):
    print("Nmap scan...",end="\r")
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
    
    pattern = r'(\d+)\/(\w+)\s+(\w+)\s+([\w\.\-\s]+)'
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
    print("Nmap scan done !!!")
# def get_ip_censys(target):
#     with open(f'Result/{target}/ip_available_{target}.txt',"r") as file1:
#         with open(f"Result/{target}/{target}_ip/censys_{target}.txt","a") as file2:
#             for line in file1:
#                 ip= line.strip()
#                 file2.write("--------------------------------------------------\n")
#                 file2.write(f"IP scan: {ip} \n")     
#                 file2.flush()
#                 t=threading.Thread(target=os.system(f"censys search {ip} | grep port >> Result/{target}/{target}_ip/censys_{target}.txt"))

def canlam(target):
    try:
        os.makedirs(f'Result/{target}/{target}_ip', exist_ok=True)
    except FileExistsError:
        pass

    # get_ip_censys(target)
    # remove_line_regex(f"Result/{target}/{target}_ip/censys_{target}.txt", ["transport"])

    get_ip_nmap(target)
    # remove_line_regex(f"Result/{target}/{target}_ip/nmap_{target}.txt", ["Nmap","Service","Running","Host","EtherFast","exact", "Network error","Linux","up","exceed"])


