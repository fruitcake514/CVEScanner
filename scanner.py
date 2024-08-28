import os
import nmap3

def scan_network(ip_range=None):
    if ip_range is None:
        ip_ranges = os.getenv('IP_RANGE', '192.168.1.0/24').split(',')
    else:
        ip_ranges = [ip_range]

    nmap = nmap3.Nmap()
    all_results = {}
    for ip_range in ip_ranges:
        results = nmap.nmap_version_detection(ip_range.strip())
        all_results.update(results)
    
    hosts = []
    for host, data in all_results.items():
        if isinstance(data, dict):
            state_info = data.get('state', {})
            state = state_info.get('state', 'unknown')
            if state.lower() == 'up':
                ports = data.get('ports', [])
                open_ports = []
                for port in ports:
                    if port['state'] == 'open':
                        service = port.get('service', {})
                        open_ports.append({
                            'port': port['portid'],
                            'service': service.get('name', 'unknown'),
                            'version': service.get('version', 'unknown')
                        })
                hosts.append((host, state, open_ports))
    return hosts
