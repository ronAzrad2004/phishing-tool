import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

def send_email_with_attachments(recipient_email="fill_in_you_email_here", subject="Phishing Analysis Results", files= [
    ("./res/website_capture.png", "website_capture.png"),
    ("./res/whois_output.txt", "whois_output.txt"),
    ("./res/source_code.txt", "source_code.txt")
]):

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))

    msg = MIMEMultipart()
    msg['From'] = os.getenv("EMAIL_USER")
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText("", "plain", "utf-8"))

    for path, name in files:
        if os.path.exists(path):
            file_ext = path.split('.')[-1].lower()
            mime_type = 'image/png' if file_ext == 'png' else 'text/plain'
            main_type, sub_type = mime_type.split('/')

            with open(path, 'rb') as f:
                part = MIMEBase(main_type, sub_type)
                part.set_payload(f.read())
            
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{name}"')
            msg.attach(part)
        else:
            print(f"Warning: {path} not found")

    smtp.sendmail(os.getenv("EMAIL_USER"), [recipient_email], msg.as_string())
    smtp.quit()
