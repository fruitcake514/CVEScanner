import logging
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
from scanner import scan_network

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/')
def dashboard():
    vulnerabilities = [
        {'host': '192.168.1.1', 'vuln': 'Open port 22'},
        {'host': '192.168.1.2', 'vuln': 'Open port 80'}
    ]
    return render_template('dashboard.html', vulnerabilities=vulnerabilities)

@app.route('/scan', methods=['POST'])
def on_demand_scan():
    ip_range = request.form['ip_range']
    try:
        scan_results = scan_network(ip_range)
        hosts = [{'ip': host, 'status': state, 'open_ports': open_ports} for host, state, open_ports in scan_results]
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
            'SMTP_PASSWORD': request.form['smtp_password']
        }
        with open('smtp_settings.json', 'w') as f:
            json.dump(smtp_settings, f)
        return redirect(url_for('dashboard'))
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
