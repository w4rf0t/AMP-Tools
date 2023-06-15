import json
import os
import sys
from threading import Thread
import requests
import re
from urllib3.exceptions import InsecureRequestWarning
import warnings
warnings.simplefilter('ignore',InsecureRequestWarning)

sensitive_data=[]
patterns = {
    'google_api'     : r'AIza[0-9A-Za-z-_]{35}',
    'google_captcha' : r'6L[0-9A-Za-z-_]{38}|^6[0-9a-zA-Z_-]{39}$',
    'google_oauth'   : r'ya29\.[0-9A-Za-z\-_]+',
    'amazon_aws_access_key_id' : r'A[SK]IA[0-9A-Z]{16}',
    'amazon_mws_auth_toke' : r'amzn\\.mws\\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
    'amazon_aws_url' : r's3\.amazonaws.com[/]+|[a-zA-Z0-9_-]*\.s3\.amazonaws.com',
    'facebook_access_token' : r'EAACEdEose0cBA[0-9A-Za-z]+',
    'authorization_basic' : r'basic\s*[a-zA-Z0-9=:_\+\/-]+',
    'authorization_bearer' : r'bearer\s*[a-zA-Z0-9_\-\.=:_\+\/]+',
    'authorization_api' : r'api[key|\s*]+[a-zA-Z0-9_\-]+',
    'mailgun_api_key' : r'key-[0-9a-zA-Z]{32}',
    'twilio_api_key' : r'SK[0-9a-fA-F]{32}',
    'twilio_account_sid' : r'AC[a-zA-Z0-9_\-]{32}',
    'twilio_app_sid' : r'AP[a-zA-Z0-9_\-]{32}',
    'paypal_braintree_access_token' : r'access_token\$production\$[0-9a-z]{16}\$[0-9a-f]{32}',
    'square_oauth_secret' : r'sq0csp-[ 0-9A-Za-z\-_]{43}|sq0[a-z]{3}-[0-9A-Za-z\-_]{22,43}',
    'square_access_token' : r'sqOatp-[0-9A-Za-z\-_]{22}|EAAA[a-zA-Z0-9]{60}',
    'stripe_standard_api' : r'sk_live_[0-9a-zA-Zhappy_urls.txt]{24}',
    'stripe_restricted_api' : r'rk_live_[0-9a-zA-Z]{24}',
    'github_access_token' : r'[a-zA-Z0-9_-]*:[a-zA-Z0-9_\-]+@github\.com*',
    'rsa_private_key' : r'-----BEGIN RSA PRIVATE KEY-----',
    'ssh_dsa_private_key' : r'-----BEGIN DSA PRIVATE KEY-----',
    'ssh_dc_private_key' : r'-----BEGIN EC PRIVATE KEY-----',
    'pgp_private_block' : r'-----BEGIN PGP PRIVATE KEY BLOCK-----',
    'json_web_token' : r'ey[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$',
    'Passwords': '/password\s*[=:]\s*[\'|"]?[A-Za-z0-9!@#$%^&*()_+{}\[\]:;<>,.?\/|\-~\\]{8,}[\'|"]?/',
    'Slack Webhooks':r'https:\/\/hooks\.slack\.com\/services\/[A-Z0-9]{10}\/[A-Z0-9]{10}\/[A-Za-z0-9]{24}',
    'Google API-key':r'AIza[0-9A-Za-z_-]{35}',
    'PayPal Client IDs':r'AY-[A-Za-z0-9_-]{22}',
    'IsAdmin':r'isadmin',
    'SSH private keys':r'/BEGIN\sRSA\sPRIVATE\shappy_urls.txtKEY|BEGIN\sPRIVATE\sKEY/',
    'Access tokens':r'/Bearer\s[a-zA-Z0-9-._~+/]+/',
    'Authorization':r'/Authorization:\s[a-zA-Z0-9-._~+/]+/',
    'Private Keys':r'/-----BEGIN (RSA|PRIVATE|OPENSSH) KEY-----[^-]*-----END (RSA|PRIVATE|OPENSSH) KEY-----/s',
    'Twilio API Keys':r'/SK[0-9a-fA-F]{32}|AC[a-z0-9]{32}/',
    'Facebook Access Tokens':r'/(?:EAACEdEose0c|EAAG|EAAK|EAAF)[A-Za-z0-9]+/',
    'Twilio Account SID':r'AC[a-z0-9]{32}',
    'SendGrid API Key':r'SG\.[a-zA-Z0-9_-]{22}\.[a-zA-Z0-9_-]{43}',
    'Mailgun API Key':r'key-[0-9a-zA-Z]{32}',
    'Stripe API Key': r'sk_live_[0-9a-zA-Z]{24}',
    'Slack Token':r'xox[baprs]-([0-9a-zA-Z]{10,48})?',
    'Facebook Access Token': r'EAACEdEose0cBA[0-9A-Za-z]+',
    'GitHub Access Token': r'[0-9a-f]{40}',
    'Square Access Token': r'sq0atp-[0-9A-Za-z_-]{22}',
    'Square OAuth Secret': r'sq0csp-[0-9A-Za-zhappy_urls.txt_-]{43}',
    'Twilio API Key': r'SK[0-9a-fA-F]{32}',
    'Slack Legacy Token': r'xoxp-[0-9A-Z]{10,12}-[0-9A-Za-z]{24}',
    'AWS access key':r'access_key_id\W+[A-Z0-9]{20}',
    'Firebase API key':r'firebase\W+[A-Za-z0-9_-]{39}',
    'Twilio API key':r'TWILIO_ACCOUNT_SID\W+[A-Za-z0-9]{34}',
    'Square API key':r'sq0atp-\w{22}',
    'Google Maps API key':r'AIzaSy[A-Za-z0-9_-]{33}',
    'Google OAuth client ID':r'client_id"\W*:\W*"[0-9]+-[A-Za-z0-9_]+\.apps\.googleusercontent\.com"',
    'Google Cloud Platform API key':r'AIzaSy[A-Za-z0-9_-]{33}',
    'Google reCAPTCHA API key':r'sitekehappy_urls.txty"\W*:\W*"[A-Za-z0-9_-]{40}"',
    'LinkedIn API key':r'linkedin\W+[A-Za-z0-9_-]{12}',
    'MailChimp API key':r'[0-9a-f]{32}-us[0-9]{1,2}',
    'Slack API key':r'xox[baprs]-([0-9a-zA-Z]{10,48})?',
    'AWS Access Key ID': r'AKIA[0-9A-Z]{16}',
    'Twilio API Key': r'SK[a-z0-9]{32}',
    'Twilio Account SID': r'AC[a-z0-9]{32}',
    'Google API Key': r'AIza[0-9A-Za-z_-]{35}',

}
import concurrent.futures
import queue
import threading
from timeit import default_timer as timer

def consumer(queue, event):
    
    while True:
        try:
            value = queue.get(timeout=5)
        except:
            print("Queue is empty")
            break
        print(value)
    print("complete")
    
    
    print("consumer existed")

def producer(queue, event, batch_data, function_run):
    print("produder running")
    while not event.is_set():
        for item in batch_data:
            
            data =  function_run(item)
            queue.put(data)
    print("producer existed")

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def collect_url(url_list):
    data = []
    for url in url_list:
        try:
            response = requests.get(url,timeout=4,verify=False)
            if response.status_code == 200:
                data.append(response.text)
            else:
                pass
        except:
            pass
    return data

def process_js_file(data):
    for key, values in patterns.items():
        matches = re.findall(values, data)
        
        if(matches):
            print(f'Find {key}:  {matches}')


def main_find_sensitive(collected_data:dict):
        pipeline = queue.Queue(maxsize=-1)
        event = threading.Event()
        
        devided_data = split(collected_data, 3)
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            for content in devided_data:
                executor.submit(producer, pipeline, event, content, process_js_file)
            executor.submit(consumer, pipeline, event)
            event.set()

from as_request import as_request
    
t1 = timer()
collected_data = as_request(input_file="happy_urls.txt")
main_find_sensitive(collected_data)
t2 = timer()
print("time elapsed: ", t2-t1)


def sensitives(url,f):
    try:
        response = requests.get(url,timeout=4,verify=False)
        contents = response.text
        for key, values in patterns.items():
            matches = re.findall(values, contents)
            if(matches):
                print(f'Find {key}:  {matches}')
                f.write(f'Find {key}:  {matches}\n')
                # return f'Find {key}:  {matches}'
    except:
        pass
    
def find_sensitive(target,status_data):
    print(" Start find sensitive...")
    status_data['find_sensitive']['find_sensitive'] = "0"
    with open(f"Result/{target}/status_of_function.json","w") as f:
        json.dump(status_data, f, indent=4)     
        
    with open(f'Result/{target}/recon/temp.txt', 'w') as f:
        with open(f'Result/{target                }/recon/{target}_url/js_crawl_urls.txt',"r") as file1:
            list_urls = file1.readlines()
            threads = []
            for url in list_urls:
                threads.append                (Thread(target=sensitives, args=(url,f)))
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
                # try:
                #     response = requests.get(url,timeout=4,verify=False)
                #     contents = response.text
                #     for key, values in patterns.items():
                #         matches = re.findall(values, contents)
                #         if(matches):
                #             f.write(f'Find {key}: {matches} \n')
                #             print(f'Find {key}:  {matches}')
                # except:
                #     pass
    status_data['find_sensitive']['find_sensitive'] = "1"
    with open(f"Result/{target}/status_of_function.json","w") as f:
        json.dump(status_data, f, indent=4)  
        
    os.system(f'cat Result/{target}/recon/temp.txt | uniq >> Result/{target}/recon/sensitive_data.txt; rm Result/{target}/recon/temp.txt')
    print("Finish find sensitive")
