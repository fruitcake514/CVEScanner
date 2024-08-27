# scanner.py
import nmap

def scan_network():
    nm = nmap.PortScanner()
    nm.scan(hosts='192.168.1.0/24', arguments='-sP')
    hosts = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
    return hosts
