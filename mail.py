import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
# Email credentials
SERVER = os.environ.get("SMTP_SERVER")
PORT = 587
username = os.environ.get("EMAIL")
password = os.environ.get("PASSWORD")
def send_email(body, subject, receiver = 'test@gmail.com'):
    # Create the container email message.
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = receiver
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))
    # Sending the email
    try:
        server = smtplib.SMTP(SERVER, PORT)  # Use appropriate host and port for your email provider
        server.starttls()  # Secure the connection
        server.login(username, password)  # Login to the server
        server.sendmail(msg['From'], msg['To'], msg.as_string())  # Send the email
        res = True
    except Exception as e:
        print(f"Failed to send email: {e}")
        res = False
    finally:
        server.quit()  # Logout and close connection
    return res