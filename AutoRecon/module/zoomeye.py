import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def zoomeye_login():
    login_url = "https://api.zoomeye.org/user/login"
    data = {
        "username": "tuanminhkma@gmail.com",
        "password": "**zuNHN*k2K8tEy"
    }
    try:
        response = requests.post(login_url, json=data)
        jwt_token = response.json()["access_token"]
        return jwt_token
    except:
        return None

def zoomeye(target,ip):
    jwt_token = zoomeye_login()
    while jwt_token == None:
        jwt_token = zoomeye_login()
    search_url = "https://api.zoomeye.org/host/search?query={}".format(ip)
    headers = {
            "Authorization": f"JWT {jwt_token}"
        }
    try:
        response = requests.get(search_url, headers=headers)
        json_obj = json.loads(response.text)
        ip = ip.replace(".", "_")
        with open(f"Result/{target}/recon/{target}_ip/zoomeye_{ip}.json", "w") as f:
            json.dump(json_obj, f, indent=4)
    except:
        pass