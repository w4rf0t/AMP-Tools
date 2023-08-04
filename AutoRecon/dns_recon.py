import os
import subprocess
import json
import csv

W = "\033[0m"
R = "\033[31m"
G = "\033[32m"
O = "\033[33m"
B = "\033[34m"

def dns_recon(target, status_data):
    print(B,"[*] DNS Enumerating...",end="\r")
    status_data["Sub_Recon"]["dns_recon"] = "0"
    with open(f"Result/{target}/status_of_function.json", "w") as f:
        json.dump(status_data, f, indent=4)
    dnss = subprocess.Popen('python3.10 dnsrecon/__main__.py -d '+ target + f' -j Result/{target}/recon/{target}_dns.json', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    dnss.communicate()
    print(G,"[*] DNS scan done !           ")
    subprocess._cleanup()
    
    # filename = f"{target}_dns"
    # with open(filename, "r") as file:
    #     data = json.load(file)

    # for entry in data:
    #     if "arguments" in entry:
    #         del entry["arguments"]

    # keys = set()
    # for entry in data:
    #     keys.update(entry.keys())

    # sorted_keys = sorted(keys)

    # output_filename = f"Result/{target}/recon/dns_{target}.csv"
    # with open(output_filename, "w", newline="") as csvfile:
    #     writer = csv.DictWriter(csvfile, fieldnames=sorted_keys)
    #     writer.writeheader()
    #     writer.writerows(data)

    status_data["Sub_Recon"]["dns_recon"] = "1"
    with open(f"Result/{target}/status_of_function.json", "w") as f:
        json.dump(status_data, f, indent=4)

# dns_recon(target)
