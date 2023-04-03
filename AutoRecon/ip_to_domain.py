import json
import subprocess
from termcolor import colored

def ip_To_Domain(target,status_data):
    print(colored("Reversing IP to domain...","blue"))
    status_data["ip_Recon"]["ip_to_domain"] = "0"
    with open(f"Result/{target}/status_of_function.json","w") as f:
        json.dump(status_data, f, indent=4)
    subprocess.call(f"$(which python3) AutoRecon/module/letwork.py -i {target} -o Result/{target}/recon/ip_to_domain.json", shell=True)
    status_data["ip_Recon"]["ip_to_domain"] = "1"
    with open(f"Result/{target}/status_of_function.json","w") as f:
        json.dump(status_data, f, indent=4)
    print(colored(" Reversing IP to domain done ","green"))