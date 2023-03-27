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
    print(B, 'Detecting WAF...\n')
    with open(f'Result/{target}/{target}_live.txt', "r") as file1:
        with open(f'Result/{target}/{target}_waf.json', "a+") as file2:
            for line in file1:
                line = line.strip()
                temp_filename = f'Result/{target}/{str(uuid.uuid4())}.json'
                with open(temp_filename, 'w') as temp_file:
                    subprocess.run(['wafw00f', line, '-o', temp_filename],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                with open(temp_filename, 'r') as temp_file:
                    data = json.load(temp_file)
                    json.dump(data, file2, indent=4)
                os.remove(temp_filename)
def waf_Recon(target):
    wafwoof(target)
