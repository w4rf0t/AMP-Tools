from whoisapi import *
import requests
import urllib3
from module.load_config import *
from module.check_ip import *

urllib3.disable_warnings()
config=load_config()


apiwhois =config.get('whoISXMLApiKey')
apihackertarget =config.get('hackertargetApiKey')

def DNSlookup(target):
    url = f'https://www.whoisxmlapi.com/whoisserver/DNSService?domainName={target}&apiKey={apiwhois}&type=_all&outputFormat=JSON'
    dnslookup= requests.get(url, verify=False)
    return dnslookup.json()

def GEOlookup(target):
    if is_valid_ip(target):
        url= f'https://ip-geolocation.whoisxmlapi.com/api/v1?apiKey={apiwhois}&ipAddress={target}&outputFormat=JSON'
    else:
        url= f'https://ip-geolocation.whoisxmlapi.com/api/v1?apiKey={apiwhois}&domain={target}&outputFormat=JSON'
    geolookup= requests.get(url, verify=False)
    return geolookup.json()
    
def NETblockip(target):
    if is_valid_ip(target):
        url=f'https://ip-netblocks.whoisxmlapi.com/api/v2?apiKey={apiwhois}&ip={target}&outputFormat=JSON'
    elif is_valid_asn(target):
        url=f'https://ip-netblocks.whoisxmlapi.com/api/v2?apiKey={apiwhois}&asn={target}&outputFormat=JSON'
    else:
        return "Error: Invalid input. Please provide a valid IP address or ASN."
    ipblock= requests.get(url, verify=False)
    return ipblock.json()

def REVERSEip(target):
    if is_valid_ip(target):
        url = f"https://api.hackertarget.com/reverseiplookup/?q={target}"
        if apihackertarget.get("hackertarget"):
            url += f"&apikey={apihackertarget}"
        response = requests.get(url)
        return response.text.strip()
    else:
        return "Error: Invalid input. Please provide a valid IP address"