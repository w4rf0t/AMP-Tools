import asyncio
import json
import os
import re
import subprocess
import threading
import time

W = "\033[0m"
R = "\033[31m"
G = "\033[32m"
O = "\033[33m"
B = "\033[34m"


async def run_command(command):
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return stdout, stderr

def js_Recon(target,status_data=None):
    print(B,'[*] Directory enumerating...',end="\r")
    status_data['js_Recon']['js_Recon'] = "0"
    with open(f"Result/{target}/status_of_function.json","w") as f:
        json.dump(status_data,f,indent=4)
    os.makedirs(f"Result/{target}/recon/{target}_url", exist_ok=True)

    crawled_file = f"Result/{target}/recon/{target}_url/crawl_urls.txt"
    js_crawled_file = f"Result/{target}/recon/{target}_url/js_crawl_urls.txt"
    IP_regex = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    path  = os.getcwd()
    try:
        if not IP_regex.match(target):
            # all_subdomains = f'/home/kali/Desktop/AMP-Tools/Result/happyorder.vn/recon/final_subdomain_happyorder.vn.txt'
            all_subdomains = f"{path}/Result/{target}/recon/final_subdomain_{target}.txt"
            subprocess.run(f"cat {all_subdomains} | ~/go/bin/gauplus -random-agent | sort -u | uniq >> {crawled_file}", shell=True)

        else:
            all_subdomains = f"{path}/Result/{target}/recon/{target}_live.txt"
            subprocess.run(f'cat {all_subdomains} | ~/go/bin/gauplus | sort -u | uniq >>  {crawled_file}', shell=True)
        '''
        grep js file
        '''
        subprocess.run(f"cat {crawled_file}| grep '.js$' | grep -ivE '\.json' >>  {js_crawled_file}", shell=True)


        # cmd = f"for i in ~/go/bin/gf -list;do cat {crawled_file}| ~/go/bin/gf $i | ~/go/bin/httpx -mc 200 -silent  >> Result/{target}/recon/{target}_url/$i_potential.txt ; done"
        # subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        gf_list =  ['debug_logic','idor','img-traversal','interestingEXT','interestingparams','interestingsubs','jsvar','lfi','rce','redirect','sqli','ssrf','xss','ssti']
        threads_gf = []
        for i in gf_list:
            threads_gf.append(threading.Thread(target=os.system, args=(f"cat {crawled_file}| ~/go/bin/gf {i} | ~/go/bin/httpx -mc 200 -silent  >>  Result/{target}/recon/{target}_url/{i}_potential.txt",)))
        for thread in threads_gf:
            thread.start()
        for thread in threads_gf:
            thread.join()
    except Exception as e:
        # print(e)
        pass
    # os.system(f"cat Result/{target}/recon/{target}_live.txt;while read url; do ~/.local/dirsearch -u $url --random-agent --follow-redirects --deep-recursive -x 500 -o Result/{target}/recon/{target}_url/$url-dirsearch.txt; done")
    status_data['js_Recon']['js_Recon'] = "1"
    with open(f"Result/{target}/status_of_function.json","w") as f:
        json.dump(status_data,f,indent=4)
    print(G,'[*] Directory enumerating done !')


