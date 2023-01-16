import sys
import subprocess
from threading import Thread
from AutoRecon.subfolder_recon import *
from AutoRecon.subdomain_recon import *
from AutoRecon.ip_recon import *
from AutoRecon.tech_detect import *
import os
from VulnScan.scanvuln import checkvuln


def menu():

    print('''

 █████╗ ███╗   ███╗██████╗
██╔══██╗████╗ ████║██╔══██╗
███████║██╔████╔██║██████╔╝         /-version 1.0-/
██╔══██║██║╚██╔╝██║██╔═══╝         /this tool is for educational purposes only/
██║  ██║██║ ╚═╝ ██║██║
╚═╝  ╚═╝╚═╝     ╚═╝╚═╝

    [*]   use -h or --help for help
    [*]   example: python3 main.py example.com
''')


def main(target):
    canlam2(target)
    t1 = Thread(target=js_recon, args=[target])
    t2 = Thread(target=canlam, args=[target])
    t3 = Thread(target=canlam3, args=[target])
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    checkvuln(target)


if __name__ == "__main__":
    try:
        target = sys.argv[1]
        while (target == "" or target == None or target == "-h" or target == "--help"):
            menu()
            target = input("Enter a target: ")
        if target.startswith("http") | target.startswith("https"):
            target = target.split("/")[2]
        main(target)
    except:
        menu()
        target = input("Enter a target: ")
        main(target)
