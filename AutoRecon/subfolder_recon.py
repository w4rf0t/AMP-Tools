import os
import sys




def js_recon(target):
    try:
        os.makedirs(f"AutoRecon/RESULT/{target}/{target}_url", exist_ok=True)
    except FileExistsError:
        pass
    os.system(f"cat AutoRecon/RESULT/{target}/sub_available_{target}.txt | waybackurls  >> AutoRecon/RESULT/{target}/{target}_url/full_urls.txt")
    os.system(f"AutoRecon/RESULT/{target}/{target}_url/full_urls.txt  | subjs >> AutoRecon/RESULT/{target}/{target}_url/js_urls.txt")
    os.system(f"for i in `gf -list`;do cat AutoRecon/RESULT/{target}/{target}_url/full_urls.txt | gf $i | qsreplace -a | httpx -mc 200 -silent  >> AutoRecon/RESULT/{target}/{target}_url/$i.txt ; done")
    os.system(f"cat AutoRecon/RESULT/{target}/sub_available_{target}.txt | while read url; do dirsearch.py -e php,aspx,asp,txt,bak -u $url >> AutoRecon/RESULT/{target}/{target}_url/$url-dirsearch.txt; done")


