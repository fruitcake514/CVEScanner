import os
import nmap

def scan_network():
    ip_range = os.getenv('IP_RANGE', '192.168.1.0/24')
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_range, arguments='-sP')
    hosts = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
    return hosts
