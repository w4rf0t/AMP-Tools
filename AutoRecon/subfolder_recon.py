import asyncio
import json
import os
import re
import subprocess
import tempfile
import threading
import time

W = "\033[0m"
R = "\033[31m"
G = "\033[32m"
O = "\033[33m"
B = "\033[34m"

def execute_command(command):
    subprocess.run(command, shell=True, check=True, stderr=subprocess.PIPE)
    
async def dirsearch(target,status_data=None):
    status_data['subfolder_Recon']['dirsearch'] = "0"
    with open(f"Result/{target}/status_of_function.json","w") as f:
        json.dump(status_data,f,indent=4)
    command_dirsearch =f"dirsearch -l Result/{target}/recon/{target}_live.txt --random-agent --follow-redirects -x 300-502 -t 500 -r --format=json -o Result/{target}/recon/{target}_url/dirsearch.json"
    process = await asyncio.create_subprocess_shell(command_dirsearch, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    async def output_handler():
        while True:
            chunk = await process.stdout.read(5192)  # Adjust buffer size as needed
            if not chunk:
                break
            lines = chunk.decode().splitlines()
            for line in lines:
                if line.startswith("Target") and len(line) > 15:
                    print("http"+line.split("http")[1],end="\r")
                elif line.startswith("http"):
                    print(line+"            ",end="\r")
    
    asyncio.create_task(output_handler())
    await process.wait()
    status_data['subfolder_Recon']['dirsearch'] = "1"
    with open(f"Result/{target}/status_of_function.json","w") as f:
        json.dump(status_data,f,indent=4)
    
async def js_Recon(target,status_data=None):
    status_data['subfolder_Recon']['js_Recon'] = "0"
    with open(f"Result/{target}/status_of_function.json","w") as f:
        json.dump(status_data,f,indent=4)
    crawled_file = f"Result/{target}/recon/{target}_url/crawl_urls.txt"
    js_crawled_file = f"Result/{target}/recon/{target}_url/js_crawl_urls.txt"
    IP_regex = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    try:
        if not IP_regex.match(target):
            with open(f"Result/{target}/recon/final_subdomain_{target}.txt","r") as f:
                all_subdomains = f.read()
        else:
            with open(f"Result/{target}/recon/{target}_live.txt","r") as f:
                all_subdomains = f.read()
        gauplus_cmd = [os.path.expanduser("~/go/bin/gauplus"), "-random-agent"]
        with open(crawled_file, 'a') as outfile:
            gauplus_proc = subprocess.Popen(gauplus_cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
            gauplus_output, _ = gauplus_proc.communicate(input=all_subdomains)
        sorted_unique_lines = "\n".join(sorted(set(gauplus_output.splitlines())))
        with open(crawled_file, 'w') as outfile:
            outfile.write(sorted_unique_lines)
        with open(crawled_file, 'r') as file:
            crawllines = file.read()
            
        grep_cmd = [os.path.expanduser("grep"), ".js$"]
        grep_proc = subprocess.Popen(grep_cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
        grep_output, _ = grep_proc.communicate(input=crawllines)

        grep_filter_cmd = [os.path.expanduser("grep"), "-ivE", r"\.json"]
        grep_filter_proc = subprocess.Popen(grep_filter_cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
        filtered_output, _ = grep_filter_proc.communicate(input=grep_output)

        with open(js_crawled_file, 'a') as outfile:
            outfile.write(filtered_output)
        
        gf_list =  ['debug_logic','idor','img-traversal','interestingEXT','interestingparams','interestingsubs','jsvar','lfi','rce','redirect','sqli','ssrf','xss','ssti']
        threads_gf = []
        for i in gf_list:
            command = f"cat {crawled_file}| ~/go/bin/gf {i} | ~/go/bin/httpx -mc 200 -silent  >> Result/{target}/recon/{target}_url/{i}_potential.txt 2>> /dev/null"
            thread = threading.Thread(target=execute_command, args=(command,))
            threads_gf.append(thread)
        for thread in threads_gf:
            try:
                thread.start()
            except:
                continue
        for thread in threads_gf:
            thread.join()
    except Exception as e:
        pass
    status_data['subfolder_Recon']['js_Recon'] = "1"
    with open(f"Result/{target}/status_of_function.json","w") as f:
        json.dump(status_data,f,indent=4)
    
async def subfolder_recon(target,status_data=None):
    print(B,'[*] Directory enumerating...',end="\r")
    
    with open(f"Result/{target}/status_of_function.json","w") as f:
        json.dump(status_data,f,indent=4)
    os.makedirs(f"Result/{target}/recon/{target}_url", exist_ok=True)
    
    # Create asyncio tasks for dirsearch and js_Recon
    dirsearch_task = asyncio.create_task(dirsearch(target, status_data))
    js_recon_task = asyncio.create_task(js_Recon(target, status_data))
    await asyncio.gather(dirsearch_task, js_recon_task)
    
    print(G,'[*] Directory enumerating done !')


