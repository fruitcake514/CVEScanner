# app.py
import logging
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from scanner import scan_network

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

SETTINGS_FILE = '/app/smtp/settings.json'

def load_settings():
    try:
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

@app.route('/')
def dashboard():
    try:
        with open('/app/data/scan_results.json', 'r') as f:
            scan_results = json.load(f)
    except FileNotFoundError:
        scan_results = []
    return render_template('dashboard.html', scan_results=scan_results)

@app.route('/scan', methods=['POST'])
def on_demand_scan():
    ip_range = request.form['ip_range']
    scan_type = request.form.get('scan_type', 'top_100')
    custom_ports = request.form.get('custom_ports', '')
    os_scan = request.form.get('os_scan') == 'true'
    try:
        scan_results = scan_network(ip_range, scan_type, custom_ports, os_scan)
        hosts = []
        for host, state, open_ports, operating_system in scan_results:
            host_data = {'ip': host, 'status': state, 'open_ports': [], 'os': operating_system}
            for port in open_ports:
                port_data = {
                    'port': port['port'],
                    'service': port['service'],
                    'cves': port.get('cves', ['CVE check failed'])
                }
                host_data['open_ports'].append(port_data)
            hosts.append(host_data)
        
        logging.info(f"Scan results: {hosts}")
        
        # Ensure the directory exists
        os.makedirs('/app/data', exist_ok=True)
        
        with open('/app/data/scan_results.json', 'w') as f:
            json.dump(hosts, f)
        return jsonify(hosts)
    except Exception as e:
        logging.error(f"An error occurred during the on-demand network scan: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        smtp_settings = {
            'SMTP_SERVER': request.form['smtp_server'],
            'SMTP_PORT': request.form['smtp_port'],
            'SMTP_USER': request.form['smtp_user'],
            'SMTP_PASSWORD': request.form['smtp_password'],
            'IP_RANGE': request.form['ip_range']
        }
        save_settings(smtp_settings)
        return redirect(url_for('dashboard'))
    settings = load_settings()
    return render_template('settings.html', settings=settings)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
