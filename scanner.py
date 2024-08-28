# scanner.py
import os
import nmap3
import docker
from cve_checker import check_cve

def scan_network(ip_range=None, network_type='host'):
    if network_type == 'docker':
        return scan_docker_network()
    else:
        return scan_host_network(ip_range)

def scan_host_network(ip_range=None):
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
                        service_name = service.get('name', 'unknown')
                        cves = check_cve(service_name)
                        open_ports.append({
                            'port': port['portid'],
                            'service': service_name,
                            'version': service.get('version', 'unknown'),
                            'cves': cves
                        })
                hosts.append((host, state, open_ports))
    return hosts

def scan_docker_network():
    client = docker.from_env()
    containers = client.containers.list()
    hosts = []
    for container in containers:
        container_info = container.attrs
        network_settings = container_info.get('NetworkSettings', {})
        ip_address = network_settings.get('IPAddress', 'unknown')
        if ip_address != 'unknown':
            nmap = nmap3.Nmap()
            results = nmap.nmap_version_detection(ip_address)
            for host, data in results.items():
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
                                cves = check_cve(service_name)
                                open_ports.append({
                                    'port': port['portid'],
                                    'service': service_name,
                                    'version': service.get('version', 'unknown'),
                                    'cves': cves
                                })
                        hosts.append((host, state, open_ports))
    return hosts
