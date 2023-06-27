import subprocess
import json
import csv


def dns_recon(target, status_data):
    print("Dns enumeration...")
    status_data["Sub_Recon"]["dns_recon"] = "0"
    with open(f"Result/{target}/status_of_function.json", "w") as f:
        json.dump(status_data, f, indent=4)
    
    command = ["dnsrecon", "-d", f"{target}", "-j", f"{target}_dns"]
    try:
        completed_process = subprocess.run(command, capture_output=True, text=True, check=True).stdout
        print(completed_process)
    except subprocess.CalledProcessError as e:
        print(e)
    
    filename = f"{target}_dns"
    with open(filename, "r") as file:
        data = json.load(file)


    for entry in data:
        if "arguments" in entry:
            del entry["arguments"]


    keys = set()
    for entry in data:
        keys.update(entry.keys())

    sorted_keys = sorted(keys)

    output_filename = f"Result/{target}/recon/dns_{target}.csv"
    with open(output_filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=sorted_keys)
        writer.writeheader()
        writer.writerows(data)

    status_data["Sub_Recon"]["dns_recon"] = "1"
    with open(f"Result/{target}/status_of_function.json", "w") as f:
        json.dump(status_data, f, indent=4)

# dns_recon(target)