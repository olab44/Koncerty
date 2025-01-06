from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


SERVICE_ACCOUNT_FILE = "service_account.json"
FOLDER_ID = "1ya1s2rfji2GPKjp-k3HWMkMSyNVokOIL"


def upload_to_drive(file_path: str, file_target_name: str) -> str:

    # Wczytanie danych uwierzytelniających
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/drive.file"]
    )

    service = build('drive', 'v3', credentials=credentials)

    file_metadata = {
        'name': file_target_name,
        'parents': [FOLDER_ID]
    }

    file = service.files().create(
        body=file_metadata,
        media_body=file_path,
        fields='id'
    ).execute()

    print(f"Uploaded file: {file_target_name} File ID: {file['id']}")

    return str(file['id'])
