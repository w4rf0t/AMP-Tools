#!/usr/bin/env python3

import requests
import argparse
from gevent import socket
from gevent.pool import Pool

requests.packages.urllib3.disable_warnings()


def main(domain):
    domainsNotFound = {}
    response = collectResponse(domain)
    domains = collectDomains(response)
    if len(domains) == 0:
        exit(1)

    pool = Pool(15)
    greenlets = [pool.spawn(resolve, domain) for domain in domains]
    pool.join(timeout=1)
    for greenlet in greenlets:
        result = greenlet.value
        if (result):
            for ip in result.values():
                if ip == 'none':
                    domainsNotFound.update(result)
    for i in domainsNotFound:
        print(i)

def resolve(domain):
    try:
        return({domain: socket.gethostbyname(domain)})
    except:
        return({domain: "none"})

def collectResponse(domain):
    url = 'https://crt.sh/?q=' + domain + '&output=json'
    try:
        response = requests.get(url, verify=False)
    except:
        exit(1)
    try:
        domains = response.json()
        return domains
    except:
        exit(1)


def collectDomains(response):
    domains = set()
    for domain in response:
        domains.add(domain['common_name'])
        if '\n' in domain['name_value']:
            domlist = domain['name_value'].split()
            for dom in domlist:
                domains.add(dom)
        else:
            domains.add(domain['name_value'])
    return domains


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", type=str, required=True,
                        help="domain to query for CT logs, e.g.: domain.com")
    args = parser.parse_args()
    main(args.domain)
