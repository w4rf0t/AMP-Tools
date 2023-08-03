import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def zoomeye_login():
    login_url = "https://api.zoomeye.org/user/login"
    data = {
        "username": "anduu150620@gmail.com",
        "password": "Andeptrai@156"
    }
    try:
        response = requests.post(login_url, json=data)
        jwt_token = response.json()["access_token"]
        return jwt_token
    except:
        return None


def zoomeye_host(target):
    jwt_token = zoomeye_login()
    while jwt_token == None:
        jwt_token = zoomeye_login()
    host_domain = str(target.split('.')[0])
    top_level_domain = str(target.split('.')[-1])
    query = f'hostname:"*{host_domain}*.{top_level_domain}"'
    with open(f"Result/{target}_hostname.txt", "w") as f:
        search_url = 'https://api.zoomeye.org/web/search'
        headers = {
            "Authorization": f"JWT {jwt_token}"
        }
        page = 1
        list_host = []
        while True:
            try:
                response = requests.get(
                    search_url, headers=headers, params={"query": query, "page": page, "pageSize": 20})
                json_list = json.loads(response.text).get("matches")
                for json_obj in json_list:
                    site = str(json_obj["site"])
                    site = site.split(".")
                    site = ".".join(site[1:])
                    if site not in list_host:
                        list_host.append(site)
                        f.write(site + "\n")
                page += 1
                if len(json_list) < 20:
                    break
            except:
                pass


def zoomeye_ip(target, ip):
    jwt_token = zoomeye_login()
    while jwt_token == None:
        jwt_token = zoomeye_login()
    # print("JWT token",jwt_token)
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
