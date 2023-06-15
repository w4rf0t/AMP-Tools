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

def js_Recon(target, status_data):
    print(B, 'Directory enumerating...')
    status_data['js_Recon']['js_Recon'] = "0"
    with open(f"Result/{target}/status_of_function.json", "w") as f:
        json.dump(status_data, f, indent=4)

    if not os.path.exists(f"Result/{target}/recon/{target}_url"):
        os.makedirs(f"Result/{target}/recon/{target}_url")
    crawled_file = f"Result/{target}/recon/{target}_url/crawl_urls.txt"
    js_crawled_file = f"Result/{target}/recon/{target}_url/js_crawl_urls.txt"
    IP_regex = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    try:
        if not IP_regex.match(target):
            all_subdomains = f"Result/{target}/recon/final_subdomain_{target}.txt"
            subprocess.run(["cat", all_subdomains], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            subprocess.run(["~/go/bin/gauplus", "--random-agent"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            subprocess.run(["sort", "-u"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            subprocess.run(["uniq"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            subprocess.run(["cat", f"{crawled_file}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        else:
            all_subdomains = f"Result/{target}/recon/{target}_live.txt"
            subprocess.run(["cat", all_subdomains], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            subprocess.run(["~/go/bin/gauplus"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            subprocess.run(["sort", "-u"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            subprocess.run(["uniq"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            subprocess.run(["cat", f"{crawled_file}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(["grep", "'.js$'"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(["grep", "-ivE", "'\.json'"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(["cat", f"{js_crawled_file}"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        cmd = f"for i in ~/go/bin/gf -list;do cat {crawled_file}| ~/go/bin/gf $i | ~/go/bin/httpx -mc 200 -silent  >> Result/{target}/recon/{target}_url/$i_potential.txt ; done"
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        gf_list = ['debug_logic', 'idor', 'img-traversal', 'interestingEXT', 'interestingparams', 'interestingsubs', 'jsvar', 'lfi', 'rce', 'redirect', 'sqli', 'ssrf', 'xss', 'ssti']
        threads_gf = []
        for i in gf_list:
            threads_gf.append(threading.Thread(target=subprocess.run, args=(["cat", crawled_file],), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True))
            threads_gf.append(threading.Thread(target=subprocess.run, args=(["~/go/bin/gf", i],), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True))
            threads_gf.append(threading.Thread(target=subprocess.run, args=(["~/go/bin/httpx", "-mc", "200", "-silent"],), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True))
        for thread in threads_gf:
            thread.start()
        for thread in threads_gf:
            thread.join()
    except:
        pass
    # os.system(f"cat Result/{target}/recon/{target}_live.txt;while read url; do ~/.local/dirsearch -u $url --random-agent --follow-redirects --deep-recursive -x 500 -o Result/{target}/recon/{target}_url/$url-dirsearch.txt; done")
    status_data['js_Recon']['js_Recon'] = "1"
    with open(f"Result/{target}/status_of_function.json", "w") as f:
        json.dump(status_data, f, indent=4)
    print(G, 'Directory enumerating done !')
