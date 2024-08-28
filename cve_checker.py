# cve_checker.py
import requests

def check_cve(service_name):
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keyword={service_name}"
    response = requests.get(url)
    if response.status_code == 200:
        cve_data = response.json()
        cves = [item['cve']['id'] for item in cve_data.get('vulnerabilities', [])]
        return cves
    return []
