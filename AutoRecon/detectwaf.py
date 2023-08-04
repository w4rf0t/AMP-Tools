import subprocess
import os
import uuid
import json

W = "\033[0m"
R = "\033[31m"
G = "\033[32m"
O = "\033[33m"
B = "\033[34m"

def wafwoof(target):
    print(B,'[*] Detecting WAF...',end="\r")   
    with open(f'Result/{target}/recon/{target}_live.txt', "r") as file1:
        with open(f'Result/{target}/recon/{target}_waf.json', "a") as file2:
            final_json = []
            for line in file1:
                line = line.strip()
                temp_filename = f'Result/{target}/recon/{str(uuid.uuid4())}.json'
                with open(temp_filename, 'w') as temp_file:
                    subprocess.run(['wafw00f', line, '-o', temp_filename],stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                with open(temp_filename, 'r') as temp_file:
                    try:
                        data = json.load(temp_file)
                        final_json.append(data)
                    except:
                        pass
                os.remove(temp_filename)
            json.dump(data, file2, indent=4)
def waf_Recon(target,status_data):
    status_data['waf_Recon']['wafwoof'] = "0"
    with open(f"Result/{target}/status_of_function.json","w") as f:
        json.dump(status_data, f, indent=4)
    wafwoof(target)
    status_data['waf_Recon']['wafwoof'] = "1"
    with open(f"Result/{target}/status_of_function.json","w") as f:
        json.dump(status_data, f, indent=4)
    print(G,'[*] WAF Detection Completed')
    