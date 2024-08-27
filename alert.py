import json
import smtplib
from email.mime.text import MIMEText

def send_alert(subject, body):
    with open('smtp_settings.json', 'r') as f:
        smtp_settings = json.load(f)

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_settings['SMTP_USER']
    msg['To'] = 'recipient@example.com'

    with smtplib.SMTP(smtp_settings['SMTP_SERVER'], smtp_settings['SMTP_PORT']) as server:
        server.starttls()
        server.login(smtp_settings['SMTP_USER'], smtp_settings['SMTP_PASSWORD'])
        server.sendmail(smtp_settings['SMTP_USER'], ['recipient@example.com'], msg.as_string())
