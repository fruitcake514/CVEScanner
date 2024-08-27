# alert.py
import smtplib
from email.mime.text import MIMEText

def send_alert(message):
    msg = MIMEText(message)
    msg['Subject'] = 'Network Vulnerability Alert'
    msg['From'] = 'your_email@example.com'
    msg['To'] = 'recipient@example.com'

    with smtplib.SMTP('smtp.example.com') as server:
        server.login('your_email@example.com', 'password')
        server.sendmail(msg['From'], [msg['To']], msg.as_string())
