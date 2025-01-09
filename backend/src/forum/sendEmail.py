from forum.Google import create_service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_gmail_email(recipient_email: str, subject: str, body: str):
    CLIENT_SECRET_FILE = 'service_account.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    # mimeMessage = MIMEMultipart()
    # mimeMessage['to'] = '<Receipient>@gmail.com'
    # mimeMessage['subject'] = subject
    # mimeMessage.attach(MIMEText(body, 'plain'))
    # raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    # message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
    # print(message)
    