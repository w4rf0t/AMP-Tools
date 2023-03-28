import os
import re
import subprocess
import threading

W = "\033[0m"
R = "\033[31m"
G = "\033[32m"
O = "\033[33m"
B = "\033[34m"

def js_Recon(target):
    if not os.path.exists(f"Result/{target}/{target}_url"):
        os.system(f"mkdir Result/{target}/{target}_url | chmod 777 Result/{target}/{target}_url")
    print(B,'Directory enumerating...')
    
    crawled_file = f"Result/{target}/{target}_url/crawl_urls.txt"
    js_crawled_file = f"Result/{target}/{target}_url/js_crawl_urls.txt"
    IP_regex = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    if not IP_regex.match(target):
        all_subdomains = f"Result/{target}/final_subdomain_{target}.txt"
        os.system(f"cat {all_subdomains} | ~/go/bin/gauplus -random-agent | sort -u | uniq >> {crawled_file}")
    else:
        all_subdomains = f"Result/{target}/{target}_live.txt"
        os.system(f'cat {all_subdomains} | ~/go/bin/gauplus | sort -u | uniq >> {crawled_file}')
    os.system(f"cat {crawled_file}| grep '.js' | grep -ivE '\.json'>> {js_crawled_file}")
    cmd = f"for i in ~/go/bin/gf -list;do cat {crawled_file}| ~/go/bin/gf $i | ~/go/bin/httpx -mc 200 -silent  >> Result/{target}/{target}_url/$i_potential.txt ; done"
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    gf_list =  ['debug_logic','idor','img-traversal','interestingEXT','interestingparams','interestingsubs','jsvar','lfi','rce','redirect','sqli','ssrf','xss','ssti']
    threads_gf = []
    for i in gf_list:
        threads_gf.append(threading.Thread(target=os.system, args=(f"cat {crawled_file}| ~/go/bin/gf {i} | ~/go/bin/httpx -mc 200 -silent  >> Result/{target}/{target}_url/{i}_potential.txt",)))
    for thread in threads_gf:
        thread.start()
    for thread in threads_gf:
        thread.join()
    # os.system(f"cat Result/{target}/{target}_live.txt;while read url; do ~/.local/dirsearch -u $url --random-agent --follow-redirects --deep-recursive -x 500 -o Result/{target}/{target}_url/$url-dirsearch.txt; done")

    print(G,'Directory enumerating done !')