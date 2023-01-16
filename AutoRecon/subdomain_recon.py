import subprocess
import os
import csv
import json




def call_oneforall(target):
    
    os.system(f"python3 /home/kali/OneForAll/oneforall.py --target {target} run")
    with open(f'/home/kali/OneForAll/results/{target}.csv', 'r') as file:
        reader = csv.reader(file)
        row_num = 0
        column = []
        for row in reader:
            if row_num > 0:
                column.append(row[5])
            row_num += 1
        with open(f'AutoRecon/RESULT/{target}/subdomain_{target}.txt', 'a') as file:
            file.write('\n'.join(column))   


def call_subfinder(target):
    os.system(f"subfinder -d {target} -o AutoRecon/RESULT/{target}/subdomain_{target}.txt ")

def call_knockpy(target):
    os.system(f"knockpy {target} -o AutoRecon/RESULT/{target}")
#     # xu ly json
    with open(f"AutoRecon/RESULT/{target}/{target}_.json", "r") as f:
        data = json.load(f)
#     # Get a list of all the domain names that end in ".vietnamairport.vn"
    with open(f'AutoRecon/RESULT/{target}/subdomain_{target}.txt', 'a') as file:
        for domain in data:
            if domain.endswith(f".{target}"):
                file.write(domain + "\n")

def sanitize_input(target):
    os.system(f"awk '!seen[$0]++' AutoRecon/RESULT/{target}/subdomain_{target}.txt > AutoRecon/RESULT/{target}/final_subdomain_{target}.txt ")
    os.system(f"cat AutoRecon/RESULT/{target}/final_subdomain_{target}.txt | httpx -sc -td -ip -o AutoRecon/RESULT/{target}/sub_status_{target}.txt")
    with open(f'AutoRecon/RESULT/{target}/sub_status_{target}.txt',"r") as file1:
        content = file1.readlines()
        with open(f'AutoRecon/RESULT/{target}/sub_available_{target}.txt',"w") as file2:
            with open(f'AutoRecon/RESULT/{target}/ip_available_{target}.txt',"w") as file3:
                for line in content:
                    if "200" or "301" or "302" or "403" in line:
                        file2.write(line.split("[")[0]+"\n")
                        file3.write((line.split("[")[4]).replace("]", "")+"\n")
    os.system(f"sed -i '/^[[:space:]]*$/d' AutoRecon/RESULT/{target}/sub_available_{target}.txt ; awk -i inplace '!seen[$0]++' AutoRecon/RESULT/{target}/ip_available_{target}.txt")
                    
def canlam2(target):
    try:
        if not(os.path.exists(f'AutoRecon/RESULT/{target}')):
            os.system(f"mkdir AutoRecon/RESULT/{target} | chmod 777 AutoRecon/RESULT/{target} ")
    except Exception as e:
        pass
    call_oneforall(target)
    call_subfinder(target)
    call_knockpy(target)
    sanitize_input(target)