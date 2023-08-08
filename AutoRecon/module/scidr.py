import requests
import base64
from datetime import datetime
from dateutil.relativedelta import relativedelta
import shodan
import json 
import subprocess
import re
from AutoRecon.module.load_config import *
from AutoRecon.module.check_ip import *

cidr_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d+\b'

def search_websites_on_cidr(cidr, api_key):
    try:
        api = shodan.Shodan(api_key)
        results = api.search(f"net:{cidr}")
        ip_port_list = [f"{result['ip_str']}:{result['port']}" for result in results['matches']]
        return ip_port_list
    except :
        return []

def search_hunterhow(ip, api_key):
    query = f'ip=="{ip}"'
    encoded_query = base64.urlsafe_b64encode(query.encode("utf-8")).decode('ascii')
    page = 1
    page_size = 100
    end_time = datetime.now().strftime('%Y-%m-%d')
    one_month_ago = datetime.now() - relativedelta(days=30)
    start_time = one_month_ago.strftime('%Y-%m-%d')
    url = "https://api.hunter.how/search?api-key=%s&query=%s&page=%d&page_size=%d&start_time=%s&end_time=%s" % (
        api_key, encoded_query, page, page_size, start_time, end_time
    )
    r = requests.get(url)
    data = r.json()['data']['list']
    ip_port_list = [f"{entry['ip']}:{entry['port']}" for entry in data]
    return ip_port_list

def remove_duplicates_from_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.read().splitlines()
        unique_lines = set(lines)
        with open(filename, 'w') as file:
            file.write('\n'.join(unique_lines))
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        
    
def trace_cidr(target):
    cidr_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?\b"
    if is_valid_ip(target):
        command = ["asnmap", "-i", target, "-silent"]
    else:
        command = ["asnmap", "-d", target, "-silent"]

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, _ = process.communicate()
        cidr_matches = re.findall(cidr_pattern, output)
        if cidr_matches:
            return cidr_matches
        else:
            return ["No CIDR found in the output."]
    except subprocess.CalledProcessError as e:
        print("Error occurred. Try again !!!")
        return None

def scidr(target):
    config = load_config()

    api_key_shodan = config.get('shodan_api_key')
    api_key_hunterhow = config.get('hunterhow_api_key')
    
    if api_key_shodan =="":
        api_key_shodan = input("Please enter your Shodan API key: ")
        config['shodan_api_key'] = api_key_shodan

    if api_key_hunterhow=="":
        api_key_hunterhow = input("Please enter your HunterHow API key: ")
        config['hunterhow_api_key'] = api_key_hunterhow
    save_config(config)
    
    
    cidr =re.search(cidr_pattern,target)
    if cidr:
        shodan_results = search_websites_on_cidr(target, api_key_shodan)
        hunterhow_results = search_hunterhow(target, api_key_hunterhow)
        combined_results = shodan_results + hunterhow_results
        with open(f'Result/{target}/recon/subdomain_{target}_scidr.txt', 'w') as file:
            file.write('\n'.join(combined_results)+'\n')
        remove_duplicates_from_file(f'Result/{target}/recon/subdomain_{target}_scidr.txt')
        
    else:
        asn=trace_cidr(target)
        with open(f'Result/{target}/recon/subdomain_{target}_scidr.txt', 'w') as file:
                for line in asn:
                    input_target=line.strip()
                    shodan_results = search_websites_on_cidr(input_target, api_key_shodan)
                    hunterhow_results = search_hunterhow(input_target, api_key_hunterhow)
                    combined_results =  shodan_results + hunterhow_results
                    file.write('\n'.join(combined_results)+ '\n')
        remove_duplicates_from_file(f'Result/{target}/recon/subdomain_{target}_scidr.txt')

