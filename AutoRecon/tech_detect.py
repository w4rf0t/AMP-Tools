import os
import sys
import threading


def detech_with_wad(target):
    try:
        os.makedirs(f'AutoRecon/RESULT/{target}/{target}_tech', exist_ok=True)
    except FileExistsError:
        pass
    with open(f'AutoRecon/RESULT/{target}/sub_available_{target}.txt',"r") as file1:
        os.system(f"rm AutoRecon/RESULT/{target}/{target}_tech/wad_{target}.txt")
        with open(f"AutoRecon/RESULT/{target}/{target}_tech/wad_{target}.txt","a") as file2:
            for line in file1:
                url = line.strip()
                file2.write("------------------------------------------------------------------------------\n")
                file2.flush()
                t=threading.Thread(target=os.system(f"wad -u {url}>>AutoRecon/RESULT/{target}/{target}_tech/wad_{target}.txt"))
def canlam3(target):
    detech_with_wad(target)
                
