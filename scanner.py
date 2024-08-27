import os
import nmap3  # Correct import for python3-nmap

def scan_network():
    ip_range = os.getenv('IP_RANGE', '192.168.1.0/24')
    nmap = nmap3.Nmap()
    results = nmap.scan_top_ports(ip_range)
    hosts = [(host, results[host]['state']) for host in results]
    return hosts
