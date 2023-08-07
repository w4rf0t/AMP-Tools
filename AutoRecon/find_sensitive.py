import json
import os
import sys
from threading import Thread
import requests
import re
from urllib3.exceptions import InsecureRequestWarning
import warnings
warnings.simplefilter('ignore',InsecureRequestWarning)
from .as_request import as_request


sensitive_data=[]
from .pattern import re_pattern
import concurrent.futures
import queue
import threading
from timeit import default_timer as timer

def consumer(queue, event):
    
    while True:
        try:
            value = queue.get(timeout=5)
        except:
            break
        # print(value)
    

def producer(queue, event, batch_data, function_run, file_to_write):
    while not event.is_set():
        for item in batch_data:
            
            data =  function_run(item, file_to_write)
            queue.put(data)

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

def process_js_file(data, file_to_write):
    for key, values in re_pattern.items():
        matches = re.findall(values, data)
        
        if(matches):
            # print(f'Find {key}:  {matches}')
            file_to_write.write(f'Find {key}:  {matches}\n')


def main_find_sensitive(url_list_file, file_to_write):
        collected_data = as_request(input_file=url_list_file)
        pipeline = queue.Queue(maxsize=-1)
        event = threading.Event()
        
        devided_data = split(collected_data, 3)
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            for content in devided_data:
                executor.submit(producer, pipeline, event, content, process_js_file, file_to_write)
            executor.submit(consumer, pipeline, event)
            event.set()


def sensitives(url,f):
    try:
        response = requests.get(url,timeout=4,verify=False)
        contents = response.text
        for key, values in re_pattern.items():
            matches = re.findall(values, contents)
            if(matches):
                # print(f'Find {key}:  {matches}')
                f.write(f'Find {key}:  {matches}\n')
                # return f'Find {key}:  {matches}'
    except:
        pass
    
def find_sensitive(target,status_data):
    print(" [*] Start find sensitive...",end="\r")
    status_data['find_sensitive']['find_sensitive'] = "0"
    with open(f"Result/{target}/status_of_function.json","w") as f:
        json.dump(status_data, f, indent=4)     
        
    with open(f'Result/{target}/recon/temp.txt', 'w') as f:
        '''
        call find sensitive
        '''
        main_find_sensitive(url_list_file=f"Result/{target}/recon/{target}_url/js_crawl_urls.txt", file_to_write=f)
    status_data['find_sensitive']['find_sensitive'] = "1"
    with open(f"Result/{target}/status_of_function.json","w") as f:
        json.dump(status_data, f, indent=4)  
        
    os.system(f'cat Result/{target}/recon/temp.txt | uniq >> Result/{target}/recon/sensitive_data.txt; rm Result/{target}/recon/temp.txt')
    print(" [*] Finish find sensitive !")
