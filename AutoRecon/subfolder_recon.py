import os
import sys
import requests

def run_command(command):
    os.system(command)

def js_recon(target):
    try:
        os.makedirs(f"Result/{target}/{target}_url", exist_ok=True)
    except FileExistsError:
        pass
    print('Directory enumeration')

    all_subdomains = f"Result/{target}/final_subdomain_{target}.txt"
    
    crawled_file = f"Result/{target}/{target}_url/crawl_urls.txt"
    js_crawled_file = f"Result/{target}/{target}_url/js_crawl_urls.txt"

    os.system(f"cat {all_subdomains} | ~/go/bin/gauplus -random-agent -b ttf,woff,svg,png,jpg | sort -u | uniq >> {crawled_file}")
    os.system(f"cat {crawled_file}| grep '.js' | grep -ivE '\.json'>> {js_crawled_file}")

    os.system(f"for i in `~/go/bin/gf -list`;do cat {crawled_file}| ~/go/bin/gf $i | ~/go/bin/httpx -mc 200 -silent  >> Result/{target}/{target}_url/$i_potential.txt ; done")

    os.system(f"cat Result/{target}/{target}_live.txt;while read url; do ~/.local/dirsearch -u $url --random-agent --follow-redirects --deep-recursive -x 500 -o Result/{target}/{target}_url/$url-dirsearch.txt; done")
