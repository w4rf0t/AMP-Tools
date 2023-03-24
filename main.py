import sys
import subprocess
from threading import Thread
from AutoRecon.subfolder_recon import *
from AutoRecon.subdomain_recon import *
from AutoRecon.ip_recon import *
from AutoRecon.find_sensitive import *
import os
from VulnScan.scanvuln import checkvuln


def menu():
    subprocess.call("clear", shell=True)
    print(R+'''

  █████╗ ███╗   ███╗██████╗
 ██╔══██╗████╗ ████║██╔══██╗
 ███████║██╔████╔██║██████╔╝         /-version 1.0-/
 ██╔══██║██║╚██╔╝██║██╔═══╝         /this tool is for educational purposes only/
 ██║  ██║██║ ╚═╝ ██║██║
 ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝
''' + W + '''
    [*]   use -h or --help for help
    [*]   example:''' + G + ''' python3 main.py example.com''', end='\n'+B)



def main(target):
    IP_regex = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    if not IP_regex.match(target):
        sub_Recon(target)
        t1 = Thread(target=ip_Recon, args=[target])
        t2 = Thread(target=js_recon, args=[target])
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    else:
        ip_Recon(target)
        js_recon(target)
    find_sensitive(target)
    checkvuln(target)



if __name__ == "__main__":
    W = "\033[0m"
    R = "\033[31m"
    G = "\033[32m"
    O = "\033[33m"
    B = "\033[34m"
    try:
        target = sys.argv[1]
        if (target == '-h' or target == '--help'):
            raise Exception
    except:
        menu()
        target = input(B + " Enter a target: ")
        while (target == '' or target == None):
            menu()
            target = input("Enter a target: ")
    if target.startswith("http") | target.startswith("https"):
        target = target.split("/")[2]
    try:
        os.makedirs(f'Result/{target}', exist_ok=True)
    except FileExistsError:
        pass
    main(target)
