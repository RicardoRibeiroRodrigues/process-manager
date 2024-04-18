import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

TO = "ricardorr7@al.insper.edu.br"
CC = ""
def send_email(title: str, body: str, attachment_content, filename):
    gmail_smtp = 'smtp.gmail.com'
    port = 587  # TLS
    smtp_user = os.environ.get('EMAIL_USER')
    smtp_pass = os.environ.get('EMAIL_PASS')
    if not smtp_user or not smtp_pass:
        raise ValueError("Email or password not set")
    
     # Create a multipart message
    msg = MIMEMultipart()
    Body = MIMEText(body, 'plain')
    # Add Headers
    msg['Subject'] = title
    msg['From'] = smtp_user
    msg['To'] = TO
    msg['CC'] = CC

    # Add body to email
    msg.attach(Body)
    
    # Using Shutil to Zip a Directory
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment_content)
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={filename}")
    msg.attach(part)

    servidor = smtplib.SMTP(gmail_smtp, port)
    servidor.starttls()

    servidor.login(smtp_user, smtp_pass)
    servidor.send_message(msg)

    servidor.quit()
