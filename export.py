import json
import openpyxl
import os

W = "\033[0m"
R = "\033[31m"
G = "\033[32m"
O = "\033[33m"
B = "\033[34m"

def nmap(target,workbook):
    with open(f'Result/{target}/recon/{target}_ip/nmap_{target}.json', 'r') as f:
        data = json.load(f)
    ip_ports = {}
    for item in data:
        ip = list(item.keys())[0]
        if ip not in ip_ports:
            ip_ports[ip] = []
        ip_ports[ip].append(item[ip])
    worksheet1 = workbook.active
    worksheet1.title = "IP Ports"
    worksheet1.append(('IP', 'Port', 'Protocol', 'Status', 'Service'))
    for cell in worksheet1[1]:
        cell.font = openpyxl.styles.Font(bold=True)
    for ip, ports in ip_ports.items():
        for port in ports:
            row = (ip, port['port'], port['protocol'],
                port['status'], port['service'])
            worksheet1.append(row)
            
def waf(target,workbook):
    worksheet2 = workbook.create_sheet(title="Firewalls")
    worksheet2.append(('URL', 'Detected', 'Firewall', 'Manufacturer'))
    for cell in worksheet2[1]:
        cell.font = openpyxl.styles.Font(bold=True)
    with open(f'Result/{target}/recon/{target}_waf.json', 'r') as f:
        text = f.read()
        records = text.split('\n][')
        for i, record in enumerate(records, 2): 
            fields = json.loads(record.strip('[]\n'))
            url = fields['url']
            detected = fields['detected']
            firewall = fields['firewall']
            manufacturer = fields['manufacturer']
            worksheet2[f'A{i}'] = url
            worksheet2[f'B{i}'] = detected
            worksheet2[f'C{i}'] = firewall
            worksheet2[f'D{i}'] = manufacturer

def hosting(target,workbook):      
    worksheet3 = workbook.create_sheet(title="Hosting")
    worksheet3.append(('IP', 'Domain'))
    for cell in worksheet3[1]:
        cell.font = openpyxl.styles.Font(bold=True)
    with open(f'Result/{target}/recon/ip_to_domain_{target}.json', 'r') as f:
        data = json.load(f)
        ip = data['ip']
        domains = data['domain'].split('\n')
        for domain in domains:
            worksheet3.append((ip, domain.strip()))

def final(target,workbook):
    with open(f'Result/{target}/recon/final_status_{target}.json', 'r') as f:
        data = json.load(f)
    worksheet4 = workbook.create_sheet(title="Status")
    worksheet4.append(('Website', 'Host', 'Port', 'Scheme', 'Title', 'Tech'))
    for cell in worksheet4[1]:
        cell.font = openpyxl.styles.Font(bold=True)
    for item in data:
        website = list(item.keys())[0]
        host = item[website]['host']
        port = item[website]['port']
        scheme = item[website]['scheme']
        title = item[website]['title']
        tech = ', '.join(item[website]['tech'])
        row = (website, host, port, scheme, title, tech)
        worksheet4.append(row)
        
def subdomains(target,workbook):   
    with open(f'Result/{target}/recon/final_subdomain_{target}.txt', 'r') as f:
        text = f.read().splitlines()
    worksheet5 =workbook.create_sheet(title="Final Subdomains")
    worksheet5.append(('Subdomain',))
    for cell in worksheet5[1]:
        cell.font = openpyxl.styles.Font(bold=True)
    for domain in text:
        worksheet5.append((domain,))
        
def live(target,workbook):
    with open(f'Result/{target}/recon/{target}_live.txt', 'r') as f:
        text = f.read().splitlines()
    worksheet6 =workbook.create_sheet(title="Live Domains")
    worksheet6.append(('Live Domain',))
    for cell in worksheet6[1]:
        cell.font = openpyxl.styles.Font(bold=True)
    for live_domain in text:
        worksheet6.append((live_domain,))

def exportation_subdomain(target):
    print(W, 'RExporting Report...')
    workbook = openpyxl.Workbook()
    nmap(target,workbook)
    waf(target,workbook)
    final(target,workbook)
    subdomains(target,workbook)
    live(target,workbook)
    workbook.save(f'Result/{target}/recon/Result.xlsx')
    os.remove(f'Result/{target}/recon/{target}_ip/nmap_{target}.json')
    os.remove(f'Result/{target}/recon/{target}_waf.json')
    os.remove(f'Result/{target}/recon/final_subdomain_{target}.txt')
    os.remove(f'Result/{target}/recon/final_status_{target}.json')
    os.remove(f'Result/{target}/recon/{target}_live.txt')
    print(G, 'Export Completed')
    
def exportation_ip(target):
    print(W, 'Exporting Report...')
    workbook = openpyxl.Workbook()
    nmap(target,workbook)
    waf(target,workbook)
    hosting(target,workbook)
    workbook.save(f'Result/{target}/recon/Result.xlsx')
    os.remove(f'Result/{target}/recon/{target}_ip/nmap_{target}.json')
    os.remove(f'Result/{target}/recon/{target}_waf.json')
    os.remove(f'Result/{target}/recon/ip_to_domain_{target}.json')
    print(G, 'Export Completed')