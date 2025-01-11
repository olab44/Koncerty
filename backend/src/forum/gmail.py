import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.auth import exceptions
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
# from dotenv import load_dotenv

# load_dotenv()


CLIENT_SECRET_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
# CLIENT_ID = '67926087995-4g20kdb33tsb3hi9giebgbs42urp0se0.apps.googleusercontent.com'
# CLIENT_SECRET = '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'
# REFRESH_TOKEN = '1//04G1N7D_kUjteCgYIARAAGAQSNwF-L9IrtfFsmKmQOtExsDvSFxqn0iu1f9fsFE3m6RoeM8Btu_dqq6QD-_uci1BFrF1tGNzTC1A'

def get_access_token():
    """Uzyskanie tokenu dostępu za pomocą refresh token."""
    
    creds = Credentials.from_authorized_user_info(
        {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'refresh_token': REFRESH_TOKEN
        },
        SCOPES
    )
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    return creds


def send_mail(subject, body, to_email):
    """Wyślij e-mail za pomocą Gmail API."""
    try:
        creds = get_access_token()

        service = build('gmail', 'v1', credentials=creds)

        message = MIMEMultipart()
        message['To'] = to_email
        message['From'] = 'megalodony.pzsp2@gmail.com'
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        send_message = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
        print(f"Message sent successfully, message ID: {send_message['id']}")

    except exceptions.RefreshError:
        print("Token has expired or is invalid, need to re-authenticate.")
    except Exception as error:
        print(f"An error occurred: {error}")

