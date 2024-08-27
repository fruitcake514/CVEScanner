# cve_checker.py
import requests

def check_cve(ip):
    url = f"https://services.nvd.nist.gov/rest/json/cves/1.0?keyword={ip}"
    response = requests.get(url)
    return response.json()
