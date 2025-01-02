from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


def send_email_notification(recipient_email: str, announcement) -> None:
    sender_email = "your_email@gmail.com"  # Configure your email server
    password = "your_email_password"

    subject = "New Announcement: " + announcement.content[:30]  # Taking first 30 chars for subject
    body = f"New announcement:\n\n{announcement.content}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)
    except Exception as e:
        print(f"Error sending email: {e}")
