import requests
import urllib3
from module.load_config import *
urllib3.disable_warnings()

def get_breached_accounts(input):
    config = load_config()
    api_key = config.get('havebeenipwn')
    url = f"https://haveibeenpwned.com/api/v3/pasteaccount/{input}"    
    headers = {"hibp-api-key": api_key}
    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None
    
def get_info_1breach(input):
    
    config = load_config()
    api_key = config.get('havebeenipwn')
    url = f"https://haveibeenpwned.com/api/v3/breach/{input}"
    headers = {"hibp-api-key": api_key}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None
    
def get_info_all_breach():
    config = load_config()
    api_key = config.get('havebeenipwn')
    url = f"https://haveibeenpwned.com/api/v3/breaches"
    headers = {"hibp-api-key": api_key}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

