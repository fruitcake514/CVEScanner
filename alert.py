import os
import smtplib
from email.mime.text import MIMEText

alerts = []

def store_alert(message):
    alerts.append(message)

def get_alerts():
    return alerts

def send_alert(message):
    store_alert(message)
    if os.getenv('EMAIL_ALERTS_ENABLED', 'false').lower() == 'true':
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = os.getenv('SMTP_PORT')
        smtp_user = os.getenv('SMTP_USER')
        smtp_password = os.getenv('SMTP_PASSWORD')

        msg = MIMEText(message)
        msg['Subject'] = 'Network Vulnerability Alert'
        msg['From'] = smtp_user
        msg['To'] = 'recipient@example.com'

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(msg['From'], [msg['To']], msg.as_string())
