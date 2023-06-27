import subprocess
import os
import json
import requests

W = "\033[0m"
R = "\033[31m"
G = "\033[32m"
O = "\033[33m"
B = "\033[34m"


def call_subfinder(target, dataf):
    print(B, 'Enumerating subdomain...', "\r")
    dataf["Sub_Recon"]["call_subfinder"] = "0"
    with open(f"Result/{target}/status_of_function.json", "w") as f:
        json.dump(dataf, f, indent=4)
    # Passive
    subprocess.run(["~/go/bin/subfinder", "-d", target, "-silent", "-all", "-o", f"Result/{target}/recon/subdomain_{target}_subfinder.txt"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, shell=True)


    url = "https://api.securitytrails.com/v1/domain/{}/subdomains".format(
        target)
    headers = {
        "apikey": "qejFbjUjH2nIKYR9QEFqnDrwMH1VRKfY"
    }
    response = requests.get(url, headers=headers)  # proxies=proxies,
    subdomains = set()
    if response.status_code == 200:
        response_json = response.json()
        for subdomain in response_json["subdomains"]:
            full_subdomain = f"{subdomain}.{target}"
            subdomains.add(full_subdomain)
    else:
        pass
    with open(f"Result/{target}/recon/subdomain_{target}_securitytraials.txt", "a") as f:
        for subdomain in subdomains:
            f.write("%s\n" % subdomain)
    dataf["Sub_Recon"]["call_subfinder"] = "1"
    with open(f"Result/{target}/status_of_function.json", "w") as f:
        json.dump(dataf, f, indent=4)


def sanitize_input(target):
    os.system(
        f"cat Result/{target}/recon/subdomain_{target}_* >> Result/{target}/recon/subdomain_{target}.txt; rm Result/{target}/recon/subdomain_{target}_*.txt ")
    os.system(
        f"awk '!seen[$0]++' Result/{target}/recon/subdomain_{target}.txt > Result/{target}/recon/final_subdomain_{target}.txt; rm Result/{target}/recon/subdomain_{target}.txt ")

    command_probe = [
        f"cat Result/{target}/recon/final_subdomain_{target}.txt | ~/go/bin/httprobe >>  Result/{target}/recon/{target}_live.txt"]
    subprocess.run(command_probe, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True)

    command_httpx = [
        f"cat Result/{target}/recon/{target}_live.txt | ~/go/bin/httpx -sc -td -ip -server -nc -json -o Result/{target}/recon/final_status_{target}.json"]
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
        try:
            tech = data['tech']
        except:
            tech = None
        try:
            title = data['title']
        except:
            title = None
        object = {data['url'].split("//")[1].split(":")[0]: {'host': host,
                                                             'port': port, 'scheme': scheme, 'tech': tech, 'title': title}}
        finaldata.append(object)
    with open(f'Result/{target}/recon/final_status_{target}.json', 'w', encoding='utf-8') as f:
        json.dump(finaldata, f, indent=4, ensure_ascii=False)
    subprocess.call(f'rm -f Result/{target}/recon/{target}_RESULT.json',
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

def sub_Recon(target):
    with open(f'Result/{target}/status_of_function.json', 'r') as f:
        dataf = json.load(f)
        call_subfinder(target, dataf)
    dataf["Sub_Recon"]["sanitize_input"] = "0"
    with open(f"Result/{target}/status_of_function.json", "w") as f:
        json.dump(dataf, f, indent=4)

    sanitize_input(target)

    dataf["Sub_Recon"]["sanitize_input"] = "1"
    with open(f"Result/{target}/status_of_function.json", "w") as f:
        json.dump(dataf, f, indent=4)
    print(G, "Enumerating subdomain done !")
