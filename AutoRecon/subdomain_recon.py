import subprocess
import os
import csv
import json
import requests
import re
def call_subfinder(target):
    print('Enumeration subdomain')
    #Passive
    os.system(f"~/go/bin/subfinder -d {target} -silent -all -o Result/{target}/subdomain_{target}_subfinder.txt")

    #bruteforce:
    os.system(f'~/go/bin/puredns bruteforce AutoRecon/Asset/dns-subdomain.txt {target} -l 5000 -r AutoRecon/Asset/resolvers.txt -w Result/{target}/subdomain_{target}_puredns.txt  > /dev/null')

    os.system(f'cat Result/{target}/subdomain_{target}_*.txt | sort -u | uniq >> Result/{target}/subdomain_{target}.txt')
    os.system(f'rm Result/{target}/subdomain_{target}_*.txt') 

    proxies= {
        'http': 'http://209.9.37.60:8087'
    }
    url = f"https://api.securitytrails.com/v1/domain/{target}/subdomains"
    headers = {
        "APIKEY": 'QH6pLgs9U2k5mCNpnTZc6FO5K4p1xWBB'
    }
    response = requests.get(url, headers=headers, proxies=proxies)
    subdomains = set()
    if response.status_code == 200:
        response_json = response.json()
        for subdomain in response_json["subdomains"]:
            full_subdomain = f"{subdomain}.{target}"
            subdomains.add(full_subdomain)
    else:
        pass

    req = requests.get("https://crt.sh/?q=%.{d}&output=json".format(d=target))

    if req.status_code == 200:
        for subdomain in response_json["subdomains"]:
            full_subdomain = f"{subdomain}.{target}"
            subdomains.add(full_subdomain)
    else:
        pass
    with open(f"Result/{target}/subdomain_{target}_securitytraials.txt", "a") as f:
        for subdomain in subdomains:
            f.write("%s\n" % subdomain)

def sanitize_input(target):
    os.system(f"cat Result/{target}/subdomain_{target}_* >> Result/{target}/subdomain_{target}.txt; rm ")
    os.system(f"awk '!seen[$0]++' Result/{target}/subdomain_{target}.txt > Result/{target}/final_subdomain_{target}.txt ")

    os.system(f"cat Result/{target}/final_subdomain_{target}.txt | ~/go/bin/httpx -sc -td -ip -o Result/{target}/sub_status_{target}.txt")

    with open(f'Result/{target}/sub_status_{target}.txt',"r") as file1:
        content = file1.readlines()
        with open(f'Result/{target}/sub_available_{target}.txt',"w") as file2:
            with open(f'Result/{target}/ip_available_{target}.txt',"w") as file3:
                for line in content:
                    if "200" or "301" or "302" or "403" in line:
                        file2.write(line.split("[")[0]+"\n")
                        file3.write((line.split("[")[4]).replace("]", "")+"\n")
    os.system(f"sed -i '/^[[:space:]]*$/d' Result/{target}/sub_available_{target}.txt ; awk -i inplace '!seen[$0]++' Result/{target}/ip_available_{target}.txt")
    os.system(f'rm Result/{target}/sub_status_{target}.txt')
def canlam2(target):
    try:
        if not(os.path.exists(f'Result/{target}')):
            os.system(f"mkdir Result/{target} | chmod 777 Result/{target} ")
    except Exception as e:
        pass
    call_subfinder(target)
    sanitize_input(target)
