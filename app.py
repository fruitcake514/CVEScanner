from flask import Flask, render_template, request, redirect, url_for
from scanner import scan_network
from cve_checker import check_cve
from alert import send_alert, store_alert, get_alerts

app = Flask(__name__)
email_alerts_enabled = False

@app.route('/')
def dashboard():
    hosts = scan_network()
    vulnerabilities = {host: check_cve(host) for host, status in hosts if status == 'up'}
    alerts = get_alerts()
    return render_template('dashboard.html', hosts=hosts, vulnerabilities=vulnerabilities, alerts=alerts, email_alerts_enabled=email_alerts_enabled)

@app.route('/toggle_email_alerts', methods=['POST'])
def toggle_email_alerts():
    global email_alerts_enabled
    email_alerts_enabled = not email_alerts_enabled
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
