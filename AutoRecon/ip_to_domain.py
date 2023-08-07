import json
# import subprocess
from termcolor import colored
import requests

def reverse_ip_lookup_hackertarget(ip):
    url = f"https://api.hackertarget.com/reverseiplookup/?q={ip}&apikey=9c86e2dc2ec96b723fb9c7e4a1de64469a19cf5d4042526ca15e3dd6ee38ae9e9ff8a6a4ba1b1031"
    response = requests.get(url)
    return response.text.strip()

def ip_To_Domain(target,status_data):
    print(colored(" [*] Reversing IP to domain...","blue"),end="\r")
    status_data["ip_Recon"]["ip_to_domain"] = "0"
    with open(f"Result/{target}/status_of_function.json","w") as f:
        json.dump(status_data, f, indent=4)
    # subprocess.Popen(f"$(which python3) AutoRecon/module/letwork.py -i {target} -o Result/{target}/recon/ip_to_domain.json", shell=True)
    # reverse_ip_lookup_hackertarget(target)
    with open(f"Result/{target}/recon/ip_to_domain.json", "w") as f:
            json.dump({"ip": target, "domain": reverse_ip_lookup_hackertarget(target)}, f, indent=4)
    status_data["ip_Recon"]["ip_to_domain"] = "1"
    with open(f"Result/{target}/status_of_function.json","w") as f:
        json.dump(status_data, f, indent=4)
    print(colored(" [*] Reversing IP to domain done ","green"))