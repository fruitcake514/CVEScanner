# cve_checker.py
import logging
import requests

def check_cve(service_name, version):
    logging.info(f"Querying CVE API for service: {service_name}, version: {version}")
    # Example API call (replace with actual API call)
    response = requests.get(f"https://cveapi.example.com/{service_name}/{version}")
    if response.status_code == 200:
        return response.json().get('cves', [])
    else:
        logging.error(f"Failed to fetch CVEs for service: {service_name}, version: {version}")
        return []
