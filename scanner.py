import os
import nmap3
import logging
from cve_checker import check_cve

logging.basicConfig(level=logging.INFO)

def scan_network(ip_range=None, scan_type='top_100', custom_ports='', os_scan=False):
    return scan_host_network(ip_range, scan_type, custom_ports, os_scan)

def scan_host_network(ip_range=None, scan_type='top_100', custom_ports='', os_scan=False):
    if ip_range is None:
        ip_ranges = os.getenv('IP_RANGE', '192.168.1.0/24').split(',')
    else:
        ip_ranges = [ip_range]

    nmap = nmap3.Nmap()
    all_results = {}
    for ip_range in ip_ranges:
        args = get_nmap_args(scan_type, custom_ports, os_scan)
        logging.info(f"Scanning IP range: {ip_range} with args: {args}")
        results = nmap.nmap_version_detection(ip_range.strip(), args=args)
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
                        service_name = service.get('name', 'unknown')
                        product = service.get('product', '')
                        version = service.get('version', '')
                        
                        # Combine product, name, and version for a more accurate service description
                        full_service = f"{product} {service_name} {version}".strip()
                        
                        try:
                            cves = check_cve(service_name, version)
                        except Exception as e:
                            logging.error(f"Error checking CVEs: {str(e)}")
                            cves = []
                        open_ports.append({
                            'port': port['portid'],
                            'service': full_service,
                            'cves': cves
                        })
                os_info = data.get('osmatch', [])
                os = os_info[0].get('name', 'Unknown') if os_info else 'Unknown'
                hosts.append((host, state, open_ports, os))
    return hosts

def get_nmap_args(scan_type, custom_ports, os_scan):
    base_args = "-sV -sC"  # Always use version detection and default scripts
    if os_scan:
        base_args += " -O"  # Add OS detection if requested
    if scan_type == 'top_100':
        return f"{base_args} -F"
    elif scan_type == 'top_1000':
        return f"{base_args}"  # Default nmap behavior
    elif scan_type == 'top_10000':
        return f"{base_args} --top-ports 10000"
    elif scan_type == 'all':
        return f"{base_args} -p-"
    elif scan_type == 'custom':
        cleaned_ports = custom_ports.replace(" ", "")  # Remove any spaces
        return f"{base_args} -p{cleaned_ports}"  # Remove space between -p and ports
    else:
        return f"{base_args} -F"  # Default to top 100 if unknown option
