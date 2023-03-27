import subprocess
import os
import json
import requests

W = "\033[0m"
R = "\033[31m"
G = "\033[32m"
O = "\033[33m"
B = "\033[34m"

def call_subfinder(target):
    print(B,'Enumerating subdomain...',"\r")
    #Passive
    os.system(f"~/go/bin/subfinder -d {target} -silent -all -o Result/{target}/subdomain_{target}_subfinder.txt 2>&1 >/dev/null")

    proxies= {
        'http': 'http://209.9.37.60:8087'
    }
    url = f"https://api.securitytrails.com/v1/domain/{target}/subdomains"
    headers = {
        "APIKEY": 'Tkoxcj2BbGXLwCZyFjpYyOJGaJd9XokP'
    }
    response = requests.get(url, headers=headers, proxies=proxies, verify=True)
    subdomains = set()
    if response.status_code == 200:
        response_json = response.json()
        for subdomain in response_json["subdomains"]:
            full_subdomain = f"{subdomain}.{target}"
            subdomains.add(full_subdomain)
    else:
        pass
    with open(f"Result/{target}/subdomain_{target}_securitytraials.txt", "a") as f:
        for subdomain in subdomains:
            f.write("%s\n" % subdomain)
def get_from_cert(target):
    command_1 = [f"python3 AutoRecon/module/crtsh_enum_psql.py {target} >> Result/{target}/subdomain_{target}_cert.txt"]
    subprocess.run(command_1, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL, shell=True)

    command_2 = [f"python3 AutoRecon/module/crtsh_enum_web.py {target} >> Result/{target}/subdomain_{target}_cert.txt"]
    subprocess.run(command_2, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL, shell=True)

    command_3 = [f"python3 AutoRecon/module/san_subdomain_enum.py {target} >> Result/{target}/subdomain_{target}_cert.txt"]
    subprocess.run(command_3, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL, shell=True)

    command_4 = [f"sh AutoRecon/module/crtsh_enum_psql.sh {target} >> Result/{target}/subdomain_{target}_cert.txt"]
    subprocess.run(command_4, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL, shell=True)
def sanitize_input(target):
    
    os.system(f"cat Result/{target}/subdomain_{target}_* >> Result/{target}/subdomain_{target}.txt; rm Result/{target}/subdomain_{target}_*.txt ")
    os.system(f"awk '!seen[$0]++' Result/{target}/subdomain_{target}.txt > Result/{target}/final_subdomain_{target}.txt; rm Result/{target}/subdomain_{target}.txt ")

    command_probe = [f"cat Result/{target}/final_subdomain_{target}.txt | ~/go/bin/httprobe >>  Result/{target}/{target}_live.txt"]
    subprocess.run(command_probe, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL, shell=True)

    command_httpx = [f"cat Result/{target}/{target}_live.txt | ~/go/bin/httpx -sc -td -ip -server -nc -json -o Result/{target}/final_status_{target}.json"]
    subprocess.run(command_httpx, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL, shell=True)

    with open(f'Result/{target}/final_status_{target}.json', 'r') as f:
            contents = f.readlines()
    with open(f'Result/{target}/{target}_RESULT.json', 'w') as clgt:
                    clgt.write('[\n')
                    for i in contents:
                        i=i.strip()
                        clgt.write(i + ',\n') 
                    clgt.seek(clgt.tell()-2,os.SEEK_SET)
                    clgt.write('\n]')
    subprocess.call(f'rm -f Result/{target}/final_status_{target}.json', stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL, shell=True)
    with open(f'Result/{target}/{target}_RESULT.json', 'r') as f:
        datas = json.load(f)
    finaldata = []
    for data in datas:
        host = data['host']
        port = data['port']
        scheme = data['scheme']
        try:
            tech = data['tech']
        except:
            tech = None
        try:
            title = data['title']
        except:
            title = None
        object = { data['url'].split("//")[1].split(":")[0] : {'host': host, 'port': port, 'scheme': scheme, 'tech': tech, 'title': title } }
        finaldata.append(object)
    with open(f'Result/{target}/final_status_{target}.json', 'w',encoding='utf-8') as f:
        json.dump(finaldata, f, indent=4,ensure_ascii=False)
    subprocess.call(f'rm -f Result/{target}/{target}_RESULT.json', stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL, shell=True)
def sub_Recon(target):
    try:
        if not(os.path.exists(f'Result/{target}')):
            os.system(f"mkdir Result/{target} | chmod 777 Result/{target} ")
    except Exception as e:
        pass
    call_subfinder(target)
    get_from_cert(target)
    sanitize_input(target)
    print(G,"Enumerating subdomain done !")
