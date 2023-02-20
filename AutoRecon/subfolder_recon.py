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

    sub_available_file = f"Result/{target}/sub_available_{target}.txt"

    crawl_output_file = f"Result/{target}/{target}_url/crawl_urls.txt"

    os.system(f"cat Result/{target}/sub_available_{target}.txt | ~/go/bin/katana -d 4 -jc -ef css,png,svg,ico,woff,gif >> {crawl_output_file}")
    os.system(f"cat Result/{target}/{target}_url/crawl_urls.txt | grep '.js$' >> Result/{target}/{target}_url/js_urls.txt")

    os.system(f"for i in `~/go/bin/gf -list`;do cat Result/{target}/{target}_url/crawl_urls.txt | gf $i | ~/go/bin/qsreplace -a | ~/go/bin/httpx -mc 200 -silent  >> Result/{target}/{target}_url/$i.txt ; done")

    # os.system(f"cat Result/{target}/sub_available_{target}.txt | while read url; do dirsearch.py -u $url >> Result/{target}/{target}_url/$url-dirsearch.txt; done")

