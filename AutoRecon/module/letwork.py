import requests
import argparse
import json
import os
from termcolor import colored


def read_config():
    parser = argparse.ArgumentParser(description="Scan IP address to find associated domains")
    parser.add_argument("-i", "--ip", help="IP address to scan", required=True)
    parser.add_argument("-ht", "--hackertarget", help="API key for HackerTarget")
    parser.add_argument("-c", "--create-config", help="Create a configuration file for storing API keys", action="store_true")
    parser.add_argument("-o", "--output", help="Save output to JSON file")

    args = parser.parse_args()

    ip = args.ip
    api_keys = {}
    output_file = args.output
    config_file = os.path.expanduser("~/.ipscan-config.json")

    # Check for existing configuration file
    if os.path.isfile(config_file):
        with open(config_file, "r") as f:
            api_keys = json.load(f)

    # Create a new configuration file if flag is set
    if args.create_config:
        ht_api_key = input("Enter your HackerTarget API key (leave blank for none): ")
        api_keys["hackertarget"] = ht_api_key
        with open(config_file, "w") as f:
            json.dump(api_keys, f, indent=4)
        print(colored(f"Configuration file saved to {config_file} !!!","blue"))

    # Check for command-line API key
    if args.hackertarget:
        api_keys["hackertarget"] = args.hackertarget

    return (ip, api_keys,output_file)


def reverse_ip_lookup_hackertarget(ip, api_key):
    url = f"https://api.hackertarget.com/reverseiplookup/?q={ip}"
    if api_key.get("hackertarget"):
        url += "&apikey=9c86e2dc2ec96b723fb9c7e4a1de64469a19cf5d4042526ca15e3dd6ee38ae9e9ff8a6a4ba1b1031"
    response = requests.get(url)
    return response.text.strip()


if __name__ == "__main__":
    ip, api_keys,output_file = read_config()

    ht_output = reverse_ip_lookup_hackertarget(ip, api_keys)
    if output_file:
        with open(output_file, "w") as f:
            json.dump({"ip": ip, "domain": ht_output}, f)

