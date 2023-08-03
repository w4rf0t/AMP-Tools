import os
import subprocess
import json
import re
import threading
import codecs
import unicodedata
from AutoRecon.module.zoomeye import zoomeye_ip


W = "\033[0m"
R = "\033[31m"
G = "\033[32m"
O = "\033[33m"
B = "\033[34m"


def get_ip_nmap(target, status_data):
    status_data["ip_Recon"]["get_ip_nmap"] = "0"
    with open(f"Result/{target}/status_of_function.json", "w") as f:
        json.dump(status_data, f, indent=4)

    print(B, "Generating IP ports service...")
    with open(f'Result/{target}/recon/final_status_{target}.json', "r") as file1:
        datas = json.load(file1)
    IPs = []
    for data in datas:
        for key in data:
            if data[key]['host'] not in IPs:            # unique IP
                IPs.append(data[key]['host'])
    threads = []
    for ip in IPs:
        threads.append(threading.Thread(target=zoomeye_ip, args=(target, ip)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # pattern = r'(\d+)\/(\w+)\s+(\w+)\s+([\w\.\-\s]+?)\s*(?:\n|$)'
    # regex = re.compile(pattern)
    json_data = []
    with open(f'Result/{target}/recon/zoomeye_subdomain_{target}.txt', "a") as file2:
        for ip in IPs:
            ip1 = ip.replace(".", "_")
            # load json file
            with open(f"Result/{target}/recon/{target}_ip/zoomeye_{ip1}.json") as file3:
                data_json = json.load(file3)
                try:
                    for data in data_json['matches']:
                        try:
                            title = data['portinfo']['title']
                            if title is not None and len(title) > 0:
                                title[0] = codecs.decode(
                                    title[0], 'unicode_escape')
                                title[0] = title[0].encode(
                                    'latin-1').decode('utf-8')
                        except:
                            pass
                        pretty_json = {"ip": ip, "port": data['portinfo']['port'], "title": title, "service": data['portinfo']['service'],
                                    "app": data['portinfo']['app'], "extrainfo": data['portinfo']['extrainfo'], "version": data['portinfo']['version']}
                        # add json to json_data
                        json_data.append(pretty_json)
                        if pretty_json["service"] == "http" or pretty_json["service"] == "https":
                            file2.write(
                                pretty_json["ip"]+":"+str(pretty_json["port"])+"\n")
                except:
                    continue
    with open(f"Result/{target}/recon/{target}_ip/zoomeye.json", "w", encoding="utf-8") as file4:
        json.dump(json_data, file4, indent=4, ensure_ascii=False)
    subprocess.run(
        f"rm -rf Result/{target}/recon/{target}_ip/zoomeye_*.json", shell=True)

    os.system(
        f"cat Result/{target}/recon/zoomeye_subdomain_{target}.txt >> Result/{target}/recon/final_subdomain_{target}.txt")
    command_probe = [
        f"cat Result/{target}/recon/zoomeye_subdomain_{target}.txt | httprobe >>  Result/{target}/recon/{target}_live.txt"]
    subprocess.run(command_probe, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True)

    status_data["ip_Recon"]["get_ip_nmap"] = "1"
    with open(f"Result/{target}/status_of_function.json", "w") as f:
        json.dump(status_data, f, indent=4)

    print(G, "Generating IP ports service done !")


def scan_input_IP(target, status_data):
    status_data["ip_Recon"]["scan_input_IP"] = "0"
    with open(f"Result/{target}/status_of_function.json", "w") as f:
        json.dump(status_data, f, indent=4)
    print(B, "Generating IP ports service...")
    os.system(f"nmap -Pn -p- {target} >> Result/{target}/recon/{target}_ip/nmap_{target}.txt")

    pattern = r'(\d+)\/(\w+)\s+(\w+)\s+([\w\.\-\s]+?)\s*(?:\n|$)'
    regex = re.compile(pattern)
    data = []
    list_WebIP = []
    with open(f"Result/{target}/recon/{target}_ip/nmap_{target}.txt", "r") as file3:
        text_data = file3.read()
    matches = regex.findall(text_data)
    for match in matches:
        object = {target: {
            "port": match[0], "protocol": match[1], "status": match[2], "service": match[3]}}
        data.append(object)
        list_WebIP.append(str(target+':'+match[0]))
    with open(f"Result/{target}/recon/{target}_ip/nmap_{target}.json", "w") as file4:
        json.dump(data, file4)
    with open(f"Result/{target}/recon/final_subdomain_{target}.txt", "w") as file5:
        for ip in list_WebIP:
            file5.write(ip+"\n")

    command_probe = [
        f"cat Result/{target}/recon/final_subdomain_{target}.txt | httprobe >>  Result/{target}/recon/{target}_live.txt"]
    subprocess.run(command_probe, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True)
    command_httpx = [
        f"cat Result/{target}/recon/{target}_live.txt | httpx -sc -td -ip -server -nc -json -o Result/{target}/recon/final_status_{target}.json"]
    subprocess.run(command_httpx, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True)
    # with open(f"Result/{target}/recon/final_status_{target}.json", 'r') as readfile:
    #     lines = readfile.readlines()
    # fake_get_ip_nmap(target)
    zoomeye_ip(target,target)
    with open(f'Result/{target}/recon/zoomeye_subdomain_{target}.txt', "a") as file2:
        ip1 = ip.replace(".", "_").split(":")[0]
    # load json file
        with open(f"Result/{target}/recon/{target}_ip/zoomeye_{ip1}.json") as file3:
            data_json = json.load(file3)
            for data in data_json['matches']:
                try:
                    title = data['portinfo']['title']
                    if title is not None and len(title) > 0:
                        title[0] = codecs.decode(
                            title[0], 'unicode_escape')
                        title[0] = title[0].encode(
                            'latin-1').decode('utf-8')
                except:
                    pass
                pretty_json = {"ip": ip.split(":")[0], "port": data['portinfo']['port'], "title": title, "service": data['portinfo']['service'],
                                "app": data['portinfo']['app'], "extrainfo": data['portinfo']['extrainfo'], "version": data['portinfo']['version']}
                # add json to json_data
                # json_data.append(pretty_json)
                if pretty_json["service"] == "http" or pretty_json["service"] == "https":
                    file2.write(
                        pretty_json["ip"]+":"+str(pretty_json["port"])+"\n")
                # os.system(f'mv Result/{target}/recon/{target}_ip/zoomeye_{ip1}.json Result/{target}/recon/{target}_ip/zoomeye.json')
                with open(f"Result/{target}/recon/{target}_ip/zoomeye.json", "w", encoding="utf-8") as file4:
                    # data = [].append(pretty_json)
                    json.dump(pretty_json, file4, indent=4, ensure_ascii=False)
    subprocess.run(
        f"rm -rf Result/{target}/recon/{target}_ip/zoomeye_*.json", shell=True)
    status_data["ip_Recon"]["scan_input_IP"] = "1"
    with open(f"Result/{target}/status_of_function.json", "w") as f:
        json.dump(status_data, f, indent=4)
    subprocess.run(
        f"rm -rf Result/{target}/recon/{target}_ip/nmap_*.txt", shell=True)
    print(G, "Generating IP ports service done !")


def ip_Recon(target, status_data):
    if not os.path.exists(f"Result/{target}/recon/{target}_ip"):
        os.makedirs(f"Result/{target}/recon/{target}_ip")
    IP_regex = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    if not IP_regex.match(target):
        get_ip_nmap(target, status_data)
    else:
        scan_input_IP(target, status_data)
    subprocess.run(
        f"rm -rf Result/{target}/recon/zoomeye_subdomain_{target}.txt", shell=True)
