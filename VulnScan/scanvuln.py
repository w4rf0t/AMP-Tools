#!/usr/bin/python3
# phudepchai

import random
import urllib.request
import urllib.error
import urllib.parse
import subprocess
import sys
import os
import requests
import zipfile
from pathlib import Path
from socket import *
from datetime import *
import urllib3
from sys import stdout

class Printer:
    def __init__(self, data):
        stdout.write("\r\x1b[K" + data.__str__())
        stdout.flush()


def logo():
    cache_Check()
    sql_list_counter()
    lfi_list_counter()
    rce_list_counter()
    xss_list_counter()


def killpid():
    os.kill(os.getpid(), 9)


def ignoring_get(url):
    header = [line.strip() for line in open(
        "lists/header", "r", encoding="utf-8")]
    ua = random.choice(header)
    headers = {"user-agent": ua}
    try:
        try:
            response = requests.get(url, headers=headers, timeout=2)
            response.raise_for_status()
        except Exception:
            return ""
        return response.text
    except Exception as verb:
        print(str(verb))


def create_tmp_folder(self):
    from tempfile import mkdtemp

    self.temp = mkdtemp(prefix="v3n0m")
    if not self.temp.endswith(os.sep):
        self.temp += os.sep


def progressBar(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d" % (percent,
                                    len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(s)
    if readsofar >= totalsize:  # near the end
        sys.stderr.write("\n")


def download(url, file, progressBar=None):
    print("Downloading %s" % url)
    urllib.request.urlretrieve(url, file, progressBar)


def unzip(file):
    with zipfile.ZipFile(file + "", "w") as myzip:
        myzip.write(file)
    os.remove(file + "")


def f_menu(target):
    import time
    W = "\033[0m"
    R = "\033[31m"
    G = "\033[32m"
    O = "\033[33m"
    B = "\033[34m"
    global vuln_scan_count
    global vuln
    vuln_scan_count = []
    vuln = []
    logo()
    print(
        G + "===========Vuln Scanner=============\n")
    print("[1] SQL Injecion From List")
    print("[2] Admin page finder")
    print("[3] Brute Force Login Page From List")
    print("[4] XSS Scan")
    print("[5] LFI Scan")
    print("[0] Exit\n")
    chce = input(B+"Your choice: ")
    if chce == "1":
        subprocess.call("clear", shell=True)
        print(G+"====SQL Injecion From List====")
        print(B)
        urls = 'Result/' + target + '/sqli.txt'
        print("SQL Injection Scanning..")
        sql = subprocess.Popen(
            'python VulnScan/modules/sqlmap/sqlmap.py -m "'
            + urls
            + '" -dbs --output-dir VulnScan/results/sqli-test --dump-file VulnScan/results/sqli-test/result --answer=Y --threads 10 --random-agent', shell=True)
        sql.communicate()
        print("SQL Injection Scan Completed, results saved in /VulnScan/results/sqli-test")
        subprocess._cleanup()
    elif chce == "2":
        subprocess.call("clear", shell=True)
        print(G+"====Admin page finder====")
        # print(B)
        # afsite = input("Enter the site eg target.com: ")
        with open('Result/' + target + '/final_subdomain_'+target+'.txt', 'r') as f:
            print("Admin page finder scanning..")
            for line in f:
                afsite = line.strip()
                print(W+"Scanning: " + afsite)
                print(O)
                pwd = os.path.dirname(str(os.path.realpath(__file__)))
                os.system("rm -rf VulnScan/results/adminfinder/"+afsite+".txt")
                findadmin = subprocess.Popen(
                    "python3 "
                    + pwd
                    + "/modules/adminfinder.py -w "+pwd+"/lists/adminlist.txt -u "
                    + str(afsite),
                    shell=True,
                )
                findadmin.communicate()
        subprocess._cleanup()
    elif chce == "3":
        subprocess.call("clear", shell=True)
        print(G+"====Brute Force Login Page From List====")
        print(B)
        logsite = input("Enter the site with login form: ")
        logsite = logsite.replace("http://", "")
        logsite = logsite.replace("https://", "")
        domain = logsite.split("/")[0]
        action = "/"+input("Enter the action of form: ")
        username = input("Enter the id of tag contains: ")
        passwd = input("Enter the id of tag contains password: ")
        print("Brute Force Started...")
        bruteforce = subprocess.Popen('wfuzz -f VulnScan/results/loginform-test/result.json,json -z file,VulnScan/lists/passwords.txt -z file,VulnScan/lists/passwords.txt -d "' +
                                      username + '=FUZZ & ' + passwd + '=FUZ2Z"  --hc 302 404 '+domain+action, shell=True)
        bruteforce.communicate()
        print("results saved in /VulnScan/results/loginform-test/result.json")
        subprocess._cleanup()
    elif chce == "4":
        subprocess.call("clear", shell=True)
        print(G+"====XSS Scan====")
        print(B)
        xssTest(target)
    elif chce == "5":
        subprocess.call("clear", shell=True)
        lfisuite = subprocess.Popen(
            "python " "VulnScan/modules/lfisuite.py ", shell=True)
        lfisuite.communicate()
        subprocess._cleanup()
    elif chce == "0":
        print(R + "\n Exiting cleanly..")
        print(W)
        sys.exit(0)

# XSS Scan


def xssTest(target):
    XssList = 'Result/'+target+'/xss.txt'
    list1 = [
        line.strip()
        for line in open(XssList, "r", errors="ignore", encoding="utf-8")
    ]
    try:
        os.system("rm VulnScan/results/xss-test/xss-log")
    except:
        pass
    print("Starting Scan...")
    for line in list1:
        subprocess.run(['echo', 'Testing ' + line],
                       stdout=open('VulnScan/results/xss-test/xss-log', 'a'))
        xss = subprocess.Popen(
            "python "
            + "VulnScan/modules/xss-strike/xsstrike.py -u '"
            + line
            + "' --file-log-level INFO  >> VulnScan/results/xss-test/xss-log",
            shell=True)
        xss.communicate()
        subprocess._cleanup()
    print("Finished Check /VulnScan/results/xss-test/xss-log")
    with open('../../results/xss-test/xss-log', 'r') as f:
        content = f.read()
        content = content.replace("*", "")

#    Declare a global, read counter files, and if nonzero display their values.


def cache_Check():
    global cachestatus
    my_file1 = Path("results/dorks/v3n0m-lfi.txt")
    my_file2 = Path("results/dorks/v3n0m-rce.txt")
    my_file3 = Path("results/dorks/v3n0m-xss.txt")
    my_file5 = Path("results/dorks/v3n0m-sqli.txt")
    my_file4 = Path("results/dorks/IPLogList.txt")
    if (
        my_file1.is_file()
        or my_file2.is_file()
        or my_file3.is_file()
        or my_file4.is_file()
        or my_file5.is_file()
    ):
        cachestatus = "contains some things"
    else:
        cachestatus = "empty"


# This is the counter section, to displays found SQLi, LFI, XSS vulns, etc.
# Declare global count for each saved value, display value to stderr above f_menu().
#
def sql_list_counter():
    global sql_count
    try:
        f = open("results/sqlmap/v3n0m-sqli.txt", encoding="utf-8")
        l = [x for x in f.readlines() if x != "\n"]
        sql_count = len(l)
    except FileNotFoundError:
        sql_count = 0


def lfi_list_counter():
    global lfi_count
    try:
        f = open("results/lfi/v3n0m-lfi.txt", encoding="utf-8")
        l = [x for x in f.readlines() if x != "\n"]
        lfi_count = len(l)
    except FileNotFoundError:
        lfi_count = 0


def xss_list_counter():
    global xss_count
    try:
        f = open("results/xsstrike/v3n0m-xss.txt", encoding="utf-8")
        l = [x for x in f.readlines() if x != "\n"]
        xss_count = len(l)
    except FileNotFoundError:
        xss_count = 0


def rce_list_counter():
    global rce_count
    try:
        f = open("results/rce/v3n0m-rce.txt", encoding="utf-8")
        l = [x for x in f.readlines() if x != "\n"]
        rce_count = len(l)
    except FileNotFoundError:
        rce_count = 0


def checkvuln(target):

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    downloads = [
        ["https://www.cloudflare.com/ips-v4", "ips-v4", progressBar],
        ["https://www.cloudflare.com/ips-v6", "ips-v6", progressBar],
        ["http://crimeflare.net:82/domains/ipout.zip", "ipout.zip", progressBar],
    ]

    list_count = 0
    lfi_count = 0

    arg_end = "--"
    arg_eva = "+"
    colMax = 60
    endsub = 1
    gets = 0
    file = "/etc/passwd"
    ProxyEnabled = False
    menu = True
    current_version = str("433  ")
    subprocess.call("clear", shell=True)
    while True:
        f_menu(target)
