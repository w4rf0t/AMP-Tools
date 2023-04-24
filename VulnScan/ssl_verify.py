import argparse
import os
from bs4 import BeautifulSoup
import requests
from termcolor import colored
import time
import urllib3
urllib3.disable_warnings()


def check_ssl(target):
    soup = BeautifulSoup(requests.get(
        'https://www.ssllabs.com/ssltest/analyze.html?d='+target, verify=False).text, 'html.parser')
    done = True
    try:
        table = soup.find(
            'table', {'id': 'multiTable', 'border': 0, 'cellpadding': 10})
        rows = table.find_all('tr')[:-1]
        for row in rows:
            cols = row.find_all('td')
            ip, test_date, duration_time, percentage = "", "", "", ""
            if len(cols) > 4:
                try:
                    ip = " IP: "+cols[1].find('a').text.strip()
                except:
                    ip = "In Queue"
                    pass
                test_date = "Test date: " + \
                    cols[2].find_all('span')[0].text.strip()
                try:
                    duration_time = "Duration: " + \
                        cols[2].find_all('span')[
                            1].text.strip().split(" ")[1]+"s"
                except:
                    duration_time = "Duration: -"
                    done = False
                try:
                    percentage = "Grade: "+cols[3].find('div').text.strip()

                except:
                    percentage = "Progress: " + \
                        str(cols[1].find(
                            'span', {'class': 'grayText'}).text.strip().split("-")[1])
                    done = False
                print(ip, '\n', test_date, '\n',
                      duration_time, '\n', percentage, '\n---------------')
            else:
                pass
        if (done == True):
            exit
    except:
        try:
            infor = soup.find('div', {'class': 'sectionBody'}).text.strip().replace(
                "  ", "").replace("\t", "").splitlines()
            if infor[0].startswith("Overall"):
                print(infor[0]+": "+infor[1]+infor[2])
                exit
            else:
                done = False
                try:
                    infor = soup.find('div', {'id': 'warningBox'}).text.strip().replace(
                        "\t", "").splitlines()
                    print("Progress: ", infor[1],
                          "\n", infor[2].replace("\t", ""))
                except:
                    print("Error")
                    exit
        except:
            infor = soup.find('div', {'id': 'warningBox'}).text.strip()
            done = False
    return done


def menu():
    os.system('clear')
    print(colored(
        '''
 ad88888ba    ad88888ba   88                ,ad8888ba,   88                                   88
d8"     "8b  d8"     "8b  88               d8"'    `"8b  88                                   88
Y8,          Y8,          88              d8'            88                                   88
`Y8aaaaa,    `Y8aaaaa,    88              88             88,dPPYba,    ,adPPYba,   ,adPPYba,  88   ,d8
  `"""""8b,    `"""""8b,  88              88             88P'    "8a  a8P_____88  a8"     ""  88 ,a8"
        `8b          `8b  88              Y8,            88       88  8PP"""""""  8b          8888[
Y8a     a8P  Y8a     a8P  88               Y8a.    .a8P  88       88  "8b,   ,aa  "8a,   ,aa  88`"Yba,
 "Y88888P"    "Y88888P"   88888888888       `"Y8888Y"'   88       88   `"Ybbd8"'   `"Ybbd8"'  88   `Y8a''', 'green'))


if __name__ == "__main__":
    argparse = argparse.ArgumentParser()
    argparse.add_argument('-t', '--target', help='Target')
    args = argparse.parse_args()

    target = args.target
    while target is None:
        menu()
        print(colored("Enter target: ", "blue"), end="")
        target = input()
    target = target.replace(
        "https://", "").replace("http://", "").split("/")[0]

    while True:
        menu()
        print(colored("Target: ", "blue") + colored(target, "red"))
        if (check_ssl(target)):
            print("=============\nScan completed")
            break
        time.sleep(5)
