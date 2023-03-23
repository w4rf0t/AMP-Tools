#!/usr/bin/python
# Modified from averagesecurityguy
# Props to him
# https://github.com/averagesecurityguy/
#
# Command-line parser taken from from below:
# by Konrads Smelkovs (https://github.com/truekonrads)       
# 
# merger.py
# based off: http://cmikavac.net/2011/07/09/merging-multiple-nessus-scans-python-script/
# by: mastahyeti
#
# Everything glued together by _sen

import requests
import json
import time
import argparse
import os
import sys
import getpass
import xml.etree.ElementTree as etree

# Hard-coded variables
requests.packages.urllib3.disable_warnings()

verify = False
token = '9262069938b05ee5e80da2af905c647e4e99a27e269b7cab'

parser = argparse.ArgumentParser(description='Download Nesuss results in bulk / Merge Nessus files')
parser.add_argument('--url', '-u', type=str, default='localhost', help="url to nessus instance! This or --merge must be specified")
parser.add_argument('--format','-F', type=str, default="html", choices=['nessus', 'html'], help='Format of nesuss output, defaults to html')
parser.add_argument('-o', '--output', type=str, default=os.getcwd(), help='Output directory')
parser.add_argument('-m', '--merge', action='store_true', help='Merge all .nessus files in output directory')
parser.add_argument('-e', '--export', action='store_true', help='Export files')
parser.add_argument('--folder','-f', type=str, help='Scan Folder from which to download', default=0)
args = parser.parse_args()

def smart_str(x):
    if isinstance(x, unicode):
        return unicode(x).encode("utf-8")
    elif isinstance(x, int) or isinstance(x, float):
        return str(x)
    return x

def build_url(resource):
    nessus_url = "https://"+args.url+":8834"
    return '{0}{1}'.format(nessus_url, resource)

def connect(method, resource, data=None):
    """
    Send a request
    Send a request to Nessus based on the specified data. If the session token
    is available add it to the request. Specify the content type as JSON and
    convert the data to JSON format.
    """
    headers = {'X-Cookie': 'token={0}'.format(token),
               'content-type': 'application/json'}

    data = json.dumps(data)

    if method == 'POST':
        r = requests.post(build_url(resource), data=data, headers=headers, verify=verify)
    elif method == 'PUT':
        r = requests.put(build_url(resource), data=data, headers=headers, verify=verify)
    elif method == 'DELETE':
        r = requests.delete(build_url(resource), data=data, headers=headers, verify=verify)
    else:
        r = requests.get(build_url(resource), params=data, headers=headers, verify=verify)

    # Exit if there is an error.
    if r.status_code != 200:
        e = r.json()
        print(e['error'])
        sys.exit()

    # When downloading a scan we need the raw contents not the JSON data. 
    if 'download' in resource:
        return r.content
    else:
        return r.json()

def login(usr, pwd):
    """
    Login to nessus.
    """
    login = {'username': usr, 'password': pwd}
    data = connect('POST', '/session', data=login)

    print (data['token'])
    return data['token']

def logout():
    """
    Logout of nessus.
    """
    connect('DELETE', '/session')

def get_format():
    # TODO: Add support for more formats if needed
    return args.format   

def get_scans():
    """
    Get Scans from JSON data
    """
    scans_to_export = {}

    data = connect('GET', '/scans')
    all_scans = data['scans']

    # Create dictionary mapping scanid:scan_name (This case scan_name = host ip)
    folder = args.folder
    for scans in all_scans:
        if scans['folder_id'] == int(folder):
            scans_to_export[scans['id']] = smart_str(scans['name'])

    return scans_to_export

def export_status(sid, fid):
    """
    Check export status
    Check to see if the export is ready for download.
    """
    data = connect('GET', '/scans/{0}/export/{1}/status'.format(sid, fid))

    return data['status'] == 'ready'


def export(scans):
    """
    Make an export request
    Request an export of the scan results for the specified scan and
    historical run. In this case the format is hard coded as nessus but the
    format can be any one of nessus, html, pdf, csv, or db. Once the request
    is made, we have to wait for the export to be ready.
    """
    # get format for export and handle POST params
    export_format = get_format()
    params = {'format': export_format, 'chapters': 'vuln_by_host'}
    
    fids = {}
    # Create dictionary mapping scan_id:file_id (File ID is used to download the file)
    for scan_id in scans.keys():
        # Attempt to Export scans
        print("Exporting {0}".format(scans[scan_id]))
        data = connect('POST', '/scans/{0}/export'.format(scan_id), data=params)
        fids[scan_id] = data['file']
        
        while export_status(scan_id, fids[scan_id]) is False:
            time.sleep(5)

        # Attempt to Download scans
        print("Downloading {0}".format(scans[scan_id]))
        data = connect('GET', '/scans/{0}/export/{1}/download'.format(scan_id, fids[scan_id]))
        scan_name = '{0}.{1}'.format(scans[scan_id],params['format'])
        scan_name_duplicate = 0
        while True:
            if scan_name in os.listdir(args.output):
                print("Duplicate Scan Name!")
                scan_name_duplicate += 1
                scan_name = '{0}_{1}.{2}'.format(scans[scan_id], str(scan_name_duplicate), params['format'])                
            else:
                break

        print('Saving scan results to {0}.'.format(scan_name))
        with open(os.path.join(args.output, scan_name), 'w') as f:
            f.write(data)

    print("All Downloads complete!")

def merge():
    first = 1
    for fileName in os.listdir(args.output):
        fileName = os.path.join(args.output, fileName)
        if ".nessus" in fileName:
            print(":: Parsing", fileName)
            if first:
                mainTree = etree.parse(fileName)
                report = mainTree.find('Report')
                report.attrib['name'] = 'Merged Report'
                first = 0
            else:
                tree = etree.parse(fileName)
                for host in tree.findall('.//ReportHost'):
                    existing_host = report.find(".//ReportHost[@name='"+host.attrib['name']+"']")
                    if not existing_host:
                        print("adding host: " + host.attrib['name'])
                        report.append(host)
                    else:
                        for item in host.findall('ReportItem'):
                            if not existing_host.find("ReportItem[@port='"+ item.attrib['port'] +"'][@pluginID='"+ item.attrib['pluginID'] +"']"):
                                print("adding finding: " + item.attrib['port'] + ":" + item.attrib['pluginID'])
                                existing_host.append(item)
        print(":: => done.")
     
    with open(os.path.join(args.output, "nessus_merged.nessus"), 'w') as merged_file:
        mainTree.write(merged_file, encoding="utf-8", xml_declaration=True)

    print("All .nessus files merged to 'nessus_merged.nessus' file in current dir")

if __name__ == '__main__':
    # Download Files
    if args.export or args.merge:
        if args.export:
            # Login
            username = input("Username: ")
            password = getpass.getpass("Password: ")
            print('Logging in....')
            token = login(username, password)
            
            print("Getting scan List....")
            scans = get_scans()

            print('Downloading and Exporting Scans...')
            export(scans)
            # Merge files
        if args.merge:
            merge()
    else:
        print(parser.format_usage()) # removes newline + None when print_usage() is used