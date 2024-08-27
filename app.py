from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)

@app.route('/')
def dashboard():
    # Example data
    hosts = [
        {'ip': '192.168.1.1', 'status': 'up'},
        {'ip': '192.168.1.2', 'status': 'down'}
    ]
    vulnerabilities = [
        {'host': '192.168.1.1', 'vuln': 'Open port 22'},
        {'host': '192.168.1.2', 'vuln': 'Open port 80'}
    ]
    return render_template('dashboard.html', hosts=hosts, vulnerabilities=vulnerabilities)

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
    app.run(debug=True)
