import sys
import subprocess
from threading import Thread
from AutoRecon.subfolder_recon import *
from AutoRecon.subdomain_recon import *
from AutoRecon.ip_recon import *
from AutoRecon.find_sensitive import *
from AutoRecon.detectwaf import *
from AutoRecon.ip_to_domain import ip_To_Domain
from AutoRecon.levenshtein import check_plagiarism_sub
from AutoRecon.module.zoomeye import zoomeye_host
import os
import time
import asyncio
from VulnScan.scanvuln import checkvuln
from termcolor import colored
from export import *


def menu():
    subprocess.call("clear", shell=True)
    text = '''

  █████╗ ███╗   ███╗██████╗
 ██╔══██╗████╗ ████║██╔══██╗
 ███████║██╔████╔██║██████╔╝         /-version 1.0-/
 ██╔══██║██║╚██╔╝██║██╔═══╝         /this tool is for educational purposes only/
 ██║  ██║██║ ╚═╝ ██║██║             /Power by ETC Technology Systems JSC
 ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝
'''
    colors = ['magenta']
    color_index = 0

    for line in text.split('\n'):
        colored_line = ''
        for char in line:
            if char != ' ':
                colored_line += colored(char,
                                        colors[color_index % len(colors)])
                color_index += 1
            else:
                colored_line += ' '
        print(colored_line)
    print(colored('''
    [*]   use -h or --help for help
    [*]   example: python3 main.py example.com''', "white"))


def main(target):
    status_data_json_subdomain = {
        "Sub_Recon": {
            "call_subfinder": "-1",
            "get_from_cert": "-1",
            "sanitize_input": "-1"
        },
        "ip_Recon": {
            "get_ip_nmap": "-1"
        },
        "js_Recon": {
            "js_Recon": "-1"
        },
        "waf_Recon": {
            "wafwoof": "-1"
        },
        "find_sensitive": {
            "find_sensitive": "-1"
        }}

    status_data_json_ip = {
        "ip_Recon": {
            "scan_input_IP": "-1",
            "ip_to_domain": "-1",
        },
        "js_Recon": {
            "js_Recon": "-1"
        },
        "waf_Recon": {
            "wafwoof": "-1"
        },
        "find_sensitive": {
            "find_sensitive": "-1"
        }}
    try:
        if not (os.path.exists(f'Result/{target}')):
            os.makedirs(f'Result/{target}')
            os.makedirs(f'Result/{target}/recon')
            os.makedirs(f'Result/{target}/recon/vuln')
    except Exception as e:
        pass
    IP_regex = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    if not IP_regex.match(target):
        with open(f"Result/{target}/status_of_function.json", "w") as f:
            json.dump(status_data_json_subdomain, f, indent=4)
        sub_Recon(target)
        with open(f"Result/{target}/status_of_function.json", "r") as f:
            status_data = json.load(f)
        ip_Recon(target, status_data)
        asyncio.run(check_plagiarism_sub(target))
        t2 = Thread(target=js_Recon, args=[target, status_data])
        t3 = Thread(target=waf_Recon, args=[target, status_data])
        t2.start()
        t3.start()
        t2.join()
        t3.join()
        find_sensitive(target, status_data)
        exportation_subdomain(target)

    else:
        with open(f"Result/{target}/status_of_function.json", "w") as f:
            json.dump(status_data_json_ip, f, indent=4)
        with open(f"Result/{target}/status_of_function.json", "r") as f:
            status_data = json.load(f)
        ip_Recon(target, status_data)
        check_plagiarism_sub(target)
        with open(f"Result/{target}/status_of_function.json", "r") as f:
            status_data = json.load(f)
        t1 = Thread(target=waf_Recon, args=[target, status_data])
        t2 = Thread(target=js_Recon, args=[target, status_data])
        t3 = Thread(target=ip_To_Domain, args=[target, status_data])
        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()
        find_sensitive(target, status_data)
        exportation_ip(target)
    checkvuln(target)


if __name__ == "__main__":
    W = "\033[0m"
    R = "\033[31m"
    G = "\033[32m"
    O = "\033[33m"
    B = "\033[34m"
    menu()
    try:
        target = sys.argv[1]
        if (target == '-h' or target == '--help'):
            raise Exception
    except:
        target = input(colored(" Enter a target: ", "blue"))
        while (target == '' or target == None):
            menu()
            target = input("Enter a target: ")
    if target.startswith("http") | target.startswith("https"):
        target = target.split("/")[2]
    try:
        os.makedirs(f'Result/{target}', exist_ok=True)
    except FileExistsError:
        pass
    print(
        colored(f"[*] Generating wildcard host for {target}...", "green"), end="\r")
    zoomeye_host(target)
    print(
        colored(f"[*] Generating wildcard host for {target} done !", "green"))
    main(target)
    threads = []
    with open(f"Result/{target}_hostname.txt", "r") as f:
        for line in f:
            line = line.strip()
            t = Thread(target=main, args=[line])
            threads.append(t)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
