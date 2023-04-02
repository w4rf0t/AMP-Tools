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
        url += f"&apikey={api_key['hackertarget']}"
    response = requests.get(url)
    return response.text.strip()


def letwork():
    ascii_art = """
.__          __                       __    
|  |   _____/  |___  _  _____________|  | __
|  | _/ __ \   __\ \/ \/ /  _ \_  __ \  |/ /
|  |_\  ___/|  |  \     (  <_> )  | \/    < 
|____/\___  >__|   \/\_/ \____/|__|  |__|_ \\
          \/                              \/
    Power by AMP Tools | ETC Technology Systems JSC
"""

# Split the ASCII art into lines and print each line in a different color
    lines = ascii_art.split("\n")
    colors = ["red", "yellow", "green", "cyan", "blue", "magenta"]
    for i, line in enumerate(lines):
        color = colors[i % len(colors)]
        print(colored(line, color))
    ip, api_keys,output_file = read_config()

    ht_output = reverse_ip_lookup_hackertarget(ip, api_keys)
    print(colored(f"Result:","red"))
    print(f"{ht_output}\n")
    if output_file:
        with open(output_file, "w") as f:
            json.dump({"ip": ip, "domain": ht_output}, f)
        print(colored(f"Output saved to {output_file}","blue"))

