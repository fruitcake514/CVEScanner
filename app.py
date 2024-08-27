# app.py
from flask import Flask, render_template
from scanner import scan_network
from cve_checker import check_cve

app = Flask(__name__)

@app.route('/')
def dashboard():
    hosts = scan_network()
    vulnerabilities = {host: check_cve(host) for host, status in hosts if status == 'up'}
    return render_template('dashboard.html', hosts=hosts, vulnerabilities=vulnerabilities)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
